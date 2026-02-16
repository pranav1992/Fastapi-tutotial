from pydantic import BaseModel, Field, field_validator
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


class TaskAssignmentCreate(BaseModel):
    user_id: Union[UUID, str]
    task_id: Union[UUID, str]

    @field_validator("user_id", "task_id", mode="before")
    @classmethod
    def ensure_uuid(cls, value):
        if isinstance(value, UUID):
            return value

        if isinstance(value, str):
            return UUID(value)

        raise TypeError("user_id and task_id must be UUID or UUID string")


class TaskAssignmentRead(BaseModel):
    id: UUID
    user_id: Union[UUID, str]
    task_id: Union[UUID, str]
    created_at: date
    active: bool = True
    expires_at: Optional[date] = Field(default=None)

    class Config:
        orm_mode = True


class WorkLogRead(BaseModel):
    id: UUID
    user_id: UUID
    task_id: UUID
    task_assignment_id: UUID
    year: int
    month: int
    created_at: date


class WorkLogCreate(BaseModel):
    user_id: Union[UUID, str]
    task_id: Union[UUID, str]
    task_assignment_id: Union[UUID, str]
    year: int
    month: int

    @field_validator("user_id", "task_id", "task_assignment_id", mode="before")
    @classmethod
    def ensure_uuid(cls, value):
        if isinstance(value, UUID):
            return value
        if isinstance(value, str):
            return UUID(value)
        raise TypeError("WorkLog IDs must be UUID or UUID string")


class WorkLogQuery(BaseModel):
    id: Optional[UUID] = None
    user_id: Union[UUID, str]
    task_id: Union[UUID, str]
    task_assignment_id: Union[UUID, str]
    year: int
    month: int

    @field_validator("user_id", "task_id", "task_assignment_id", "id", mode="before")
    @classmethod
    def ensure_uuid(cls, value):
        if value is None:
            return value
        if isinstance(value, UUID):
            return value
        if isinstance(value, str):
            return UUID(value)
        raise TypeError("WorkLog IDs must be UUID or UUID string")


class TimeLogCreate(BaseModel):
    task_id: Union[UUID, str]
    user_id: Union[UUID, str]
    task_assignment_id: Union[UUID, str]
    worklog_id: Union[UUID, str]
    start_time: datetime
    end_time: datetime

    @field_validator("task_id", "user_id", "task_assignment_id", "worklog_id", mode="before")
    @classmethod
    def ensure_uuid(cls, value):
        if isinstance(value, UUID):
            return value
        if isinstance(value, str):
            return UUID(value)
        raise TypeError("TimeLog IDs must be UUID or UUID string")


class TimeLogRead(BaseModel):
    id: UUID
    task_id: UUID
    user_id: UUID
    task_assignment_id: UUID
    created_at: date
    start_time: datetime
    end_time: datetime
    total_time: Optional[timedelta] = None

    class Config:
        orm_mode = True
        json_encoders = {
            timedelta: lambda td: int(td.total_seconds())
        }
