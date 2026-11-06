import logging
import threading
import traceback
from datetime import datetime
from typing import Optional

from selenium.common.exceptions import TimeoutException, WebDriverException

from app.config import settings
from app.database import SessionLocal
from app.exceptions import ApplicationException, BusinessException
from app.models import AutomationTask, TaskStatus
from app.selenium_runner import run_selenium_workflow

logger = logging.getLogger(__name__)

_wake_event = threading.Event()
_stop_event = threading.Event()
_worker_thread: Optional[threading.Thread] = None
_active_task_id: Optional[str] = None
_active_task_lock = threading.Lock()


def get_current_running_task_id() -> Optional[str]:
    with _active_task_lock:
        return _active_task_id


def set_current_running_task_id(task_id: Optional[str]):
    global _active_task_id
    with _active_task_lock:
        _active_task_id = task_id


def notify_worker():
    """Wakes up the worker immediately when a new task is enqueued."""
    _wake_event.set()


def _single_worker_loop():
    """
    Continuous single-worker process.
    Claims tasks sequentially from PostgreSQL in FIFO order using FOR UPDATE SKIP LOCKED.
    Only one worker executes at any moment.
    """
    logger.info("Sequential single-worker queue started.")

    while not _stop_event.is_set():
        task_info = None
        db = SessionLocal()

        try:
            # Atomic lock of the oldest QUEUED record
            task = (
                db.query(AutomationTask)
                .filter(AutomationTask.status == TaskStatus.QUEUED)
                .order_by(AutomationTask.created_at.asc())
                .with_for_update(skip_locked=True)
                .first()
            )

            if task:
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.utcnow()
                db.commit()
                task_info = (task.id, task.account_or_record_id)
            else:
                db.rollback()

        except Exception as e:
            db.rollback()
            logger.error(f"Error querying PostgreSQL queue: {e}")
        finally:
            db.close()

        if task_info:
            task_id, record_id = task_info
            set_current_running_task_id(task_id)
            logger.info(f"Worker picked task {task_id} (Record: {record_id})")

            db = SessionLocal()
            try:
                # Executes the 10-20 min Selenium workflow synchronously
                case_notes = run_selenium_workflow(record_id)

                task = db.query(AutomationTask).filter(AutomationTask.id == task_id).first()
                if task:
                    task.status = TaskStatus.SUCCESS
                    task.case_notes = case_notes
                    task.completed_at = datetime.utcnow()
                    db.commit()
                logger.info(f"Task {task_id} completed as SUCCESS.")

            except BusinessException as be:
                task = db.query(AutomationTask).filter(AutomationTask.id == task_id).first()
                if task:
                    task.status = TaskStatus.BUSINESS_EXCEPTION
                    task.exception_type = "BusinessException"
                    task.exception_message = str(be.message)
                    task.completed_at = datetime.utcnow()
                    db.commit()
                logger.warning(f"Task {task_id} completed with BusinessException: {be.message}")

            except (WebDriverException, TimeoutException, ApplicationException, Exception) as ae:
                tb = traceback.format_exc()
                task = db.query(AutomationTask).filter(AutomationTask.id == task_id).first()
                if task:
                    task.status = TaskStatus.APPLICATION_EXCEPTION
                    task.exception_type = type(ae).__name__
                    task.exception_message = str(ae)
                    task.traceback = tb
                    task.completed_at = datetime.utcnow()
                    db.commit()
                logger.error(f"Task {task_id} completed with ApplicationException: {ae}")

            finally:
                set_current_running_task_id(None)
                db.close()

            # Immediately check for the next task in queue without waiting
            continue

        # Wait until woken up by new API call or timeout
        _wake_event.wait(timeout=settings.WORKER_POLL_INTERVAL_SECONDS)
        _wake_event.clear()

    logger.info("Sequential single-worker queue stopped.")


def start_worker():
    global _worker_thread
    if _worker_thread is None or not _worker_thread.is_alive():
        _stop_event.clear()
        _worker_thread = threading.Thread(
            target=_single_worker_loop,
            daemon=True,
            name="SequentialSeleniumWorker"
        )
        _worker_thread.start()


def stop_worker():
    _stop_event.set()
    _wake_event.set()
    if _worker_thread:
        _worker_thread.join(timeout=10)
