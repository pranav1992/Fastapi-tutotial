from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional
from uuid import UUID, uuid4


class UserData(BaseModel):
    name: str
    employee_id: str


class TaskData(BaseModel):
    name: str
    description: Optional[str] = None


class TaskResponse(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: date = Field(default_factory=date.today)
    name: str = Field(max_length=200, unique=True, index=True)
    name_lower: str = Field(max_length=200, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)


class TimeLogData(BaseModel):
    start_time: datetime
    end_time: datetime


class TaskAssignmentData(BaseModel):
    user_id: UUID
    task_id: UUID


class WorkLogDataResponse(BaseModel):
    user_id: UUID
    task_id: UUID
    year: int
    month: int


class WorkLogData(BaseModel):
    user_id: UUID
    task_id: UUID
    target_date: Optional[date] = None
