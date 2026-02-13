from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime
from .models import TaskStatus

class TaskBase(BaseModel):
    name: str
    status: TaskStatus = TaskStatus.PENDING
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

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
