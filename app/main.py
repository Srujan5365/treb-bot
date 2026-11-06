from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import authenticate
from app.config import settings
from app.database import Base, engine, get_db
from app.models import AutomationTask, TaskStatus
from app.schemas import QueueOverviewResponse, TaskResponse, TaskTriggerRequest
from app.worker import (
    get_current_running_task_id,
    notify_worker,
    start_worker,
    stop_worker,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize PostgreSQL tables
    Base.metadata.create_all(bind=engine)
    # Start single-worker queue loop
    start_worker()
    yield
    # Clean shutdown
    stop_worker()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.post(
    "/api/v1/tasks/run",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enqueue Automation Task (Strict Sequential Execution)",
)
def trigger_task(
    payload: TaskTriggerRequest,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate),
):
    """
    Enqueues a record into PostgreSQL with status QUEUED.
    The single worker will process it after the preceding task completes.
    Returns 202 Accepted and current position in queue.
    """
    new_task = AutomationTask(
        account_or_record_id=payload.account_or_record_id,
        status=TaskStatus.QUEUED,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Wake worker daemon
    notify_worker()

    # Calculate queue position
    queued_ahead = (
        db.query(AutomationTask)
        .filter(
            AutomationTask.status == TaskStatus.QUEUED,
            AutomationTask.created_at < new_task.created_at,
        )
        .count()
    )
    is_busy = get_current_running_task_id() is not None
    queue_pos = queued_ahead + (1 if is_busy else 0)

    return TaskResponse(
        task_id=new_task.id,
        account_or_record_id=new_task.account_or_record_id,
        status=new_task.status,
        created_at=new_task.created_at,
        queue_position=queue_pos,
    )


@app.get(
    "/api/v1/tasks/queue/status",
    response_model=QueueOverviewResponse,
    summary="Check Single Worker Queue State",
)
def get_queue_overview(
    db: Session = Depends(get_db),
    user: str = Depends(authenticate),
):
    """Returns whether the worker is currently executing a job and number of queued jobs."""
    active_id = get_current_running_task_id()
    queued_count = (
        db.query(AutomationTask)
        .filter(AutomationTask.status == TaskStatus.QUEUED)
        .count()
    )
    return QueueOverviewResponse(
        is_worker_busy=active_id is not None,
        current_running_task_id=active_id,
        queued_tasks_count=queued_count,
    )


@app.get(
    "/api/v1/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get Task Status and Database Outcomes",
)
def get_task_status(
    task_id: str,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate),
):
    """Poll task progress, case notes, or error details from PostgreSQL."""
    task = db.query(AutomationTask).filter(AutomationTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    queue_pos = None
    if task.status == TaskStatus.QUEUED:
        ahead = (
            db.query(AutomationTask)
            .filter(
                AutomationTask.status == TaskStatus.QUEUED,
                AutomationTask.created_at < task.created_at,
            )
            .count()
        )
        is_busy = get_current_running_task_id() is not None
        queue_pos = ahead + (1 if is_busy else 0)

    return TaskResponse(
        task_id=task.id,
        account_or_record_id=task.account_or_record_id,
        status=task.status,
        created_at=task.created_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        case_notes=task.case_notes,
        exception_type=task.exception_type,
        exception_message=task.exception_message,
        queue_position=queue_pos,
    )


@app.get(
    "/api/v1/tasks",
    response_model=List[TaskResponse],
    summary="List Recent Task Executions",
)
def list_tasks(
    limit: int = 25,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate),
):
    tasks = (
        db.query(AutomationTask)
        .order_by(AutomationTask.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        TaskResponse(
            task_id=t.id,
            account_or_record_id=t.account_or_record_id,
            status=t.status,
            created_at=t.created_at,
            started_at=t.started_at,
            completed_at=t.completed_at,
            case_notes=t.case_notes,
            exception_type=t.exception_type,
            exception_message=t.exception_message,
        )
        for t in tasks
    ]
