from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime
from .models import TaskStatus, TaskPriority

class TaskBase(BaseModel):
    name: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    customer_name: Optional[str] = None
    stakeholders: Optional[str] = None
    useful_links: Optional[str] = None
    comments: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    name: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

# Configure Pydantic behavior at runtime so we don't define both
# `Config` and `model_config` in the class body (which raises an error).

try:
    # pydantic v2's BaseModel exposes `model_config` attribute
    from pydantic import BaseModel as _PydanticBase
    _has_v2 = hasattr(_PydanticBase, "model_config")
except Exception:
    _has_v2 = False

if _has_v2:
    Task.model_config = {"from_attributes": True}
else:
    class Config:
        orm_mode = True

    Task.Config = Config


