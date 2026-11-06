from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models import TaskStatus


class TaskTriggerRequest(BaseModel):
    account_or_record_id: str


class TaskResponse(BaseModel):
    task_id: str
    account_or_record_id: str
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    case_notes: Optional[str] = None
    exception_type: Optional[str] = None
    exception_message: Optional[str] = None
    queue_position: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class QueueOverviewResponse(BaseModel):
    is_worker_busy: bool
    current_running_task_id: Optional[str] = None
    queued_tasks_count: int
