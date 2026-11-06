import enum
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Enum, Index, String, Text
from app.database import Base


class TaskStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    BUSINESS_EXCEPTION = "BUSINESS_EXCEPTION"
    APPLICATION_EXCEPTION = "APPLICATION_EXCEPTION"


class AutomationTask(Base):
    __tablename__ = "automation_tasks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_or_record_id = Column(String(100), nullable=False, index=True)
    status = Column(
        Enum(TaskStatus, name="task_status_enum"),
        default=TaskStatus.QUEUED,
        nullable=False,
        index=True,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    case_notes = Column(Text, nullable=True)
    exception_type = Column(String(100), nullable=True)
    exception_message = Column(Text, nullable=True)
    traceback = Column(Text, nullable=True)

    __table_args__ = (
        Index("ix_tasks_status_created", "status", "created_at"),
    )
