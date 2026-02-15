from pydantic import BaseModel, Field
from datetime import datetime, date, timedelta
from typing import Optional, Union
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


class TaskAssignmentData(BaseModel):
    user_id: UUID
    task_id: UUID


class WorkLogDataResponse(BaseModel):
    user_id: UUID
    task_id: UUID
    year: int
    month: int
    created_at: date


class WorkLogData(BaseModel):
    user_id: UUID
    task_id: UUID
    target_date: Optional[date] = None


class WorkLogRequest(BaseModel):
    task_assignment_id: Union[UUID, str]
    target_date: Optional[date] = None


class TimeLogCreate(BaseModel):
    task_id: UUID
    user_id: UUID
    start_time: datetime
    end_time: datetime


class TimeLogRead(BaseModel):
    id: UUID
    task_id: UUID
    user_id: UUID
    created_at: date
    start_time: datetime
    end_time: datetime
    total_time: Optional[timedelta] = None

    class Config:
        orm_mode = True
        json_encoders = {
            timedelta: lambda td: int(td.total_seconds())
        }
