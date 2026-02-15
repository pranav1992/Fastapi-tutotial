
from sqlmodel import SQLModel, Field
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, date, timedelta
from pydantic import field_validator, model_validator
from sqlalchemy import UniqueConstraint
from typing import Optional


class AdjustmentType(str, Enum):
    INCREASE = "INCREASE"
    DECREASE = "DECREASE"


class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: date = Field(default_factory=date.today)
    name: str = Field(max_length=200, unique=True, index=True)
    name_lower: str = Field(max_length=200, unique=True, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)


class WorkRate(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="user.id")
    task_id: Optional[UUID] = Field(default=None, foreign_key="task.id")

    rate_per_hour: Decimal

    valid_from: date
    valid_to: Optional[date] = Field(default=None)


class TaskAssignment(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "task_id",
            name="uq_task_assignment_user_task",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    task_id: UUID = Field(foreign_key="task.id")
    created_at: date = Field(default_factory=date.today)
    active: bool = True
    expires_at: Optional[date] = Field(default=None)

# class WorkLog(SQLModel, table=True):
#     id: UUID = Field(default_factory=uuid4, primary_key=True)
#     user_id: UUID = Field(foreign_key="user.id")
#     task_id: UUID = Field(foreign_key="task.id")
#     created_at: date = Field(default_factory=date.today)
#     start_time: datetime
#     end_time: datetime | None = None
#     active: bool = True


class WorkLog(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "task_id",
            "year",
            "month",
            name="uq_worklog_user_task_month",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="user.id")
    task_id: UUID = Field(foreign_key="task.id")

    year: int
    month: int  

    created_at: date = Field(default_factory=date.today)
    active: bool = True


class TimeLog(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # Link to the task assignment; SQLModel expects a string foreign_key
    # target, not a column object.
    task_id: UUID = Field(foreign_key="taskassignment.id")
    user_id: UUID = Field(foreign_key="user.id")
    created_at: Optional[date] = Field(default_factory=date.today)
    start_time: datetime
    end_time: datetime
    total_time: Optional[timedelta] = Field(default=None)

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, end_time, info):
        start_time = info.data.get("start_time")

        if not start_time:
            return end_time

        # 1️ end must be after start
        if end_time <= start_time:
            raise ValueError("end_time must be after start_time")

        # 2️ max duration: 12 hours
        max_duration = timedelta(hours=12)
        if end_time - start_time > max_duration:
            raise ValueError("worklog duration cannot exceed 12 hours")

        return end_time

    @model_validator(mode="after")
    def validate_and_set_total_time(self):
        # 1️ end_time cannot exist without start_time
        if self.end_time and not self.start_time:
            raise ValueError("end_time cannot be set without start_time")

        # 2️ If end_time exists, validate it
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValueError("end_time must be after start_time")

            duration = self.end_time - self.start_time

            # 3️ Max duration = 12 hours
            if duration > timedelta(hours=12):
                raise ValueError("timelog duration cannot exceed 12 hours")

            # 4️ Automatically set total_time
            self.total_time = duration

        return self


class Adjustment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    settlement_id: UUID = Field(foreign_key="worksettlement.id")

    adjustment_type: AdjustmentType  # INCREASE / DECREASE

    amount: Decimal  # always POSITIVE

    reason: str

    # Optional but VERY important for audit
    applied_from: Optional[date] = Field(default=None)
    applied_to: Optional[date] = Field(default=None)

    created_at: date = Field(default_factory=date.today)

    @field_validator("settlement_id")
    @classmethod
    def validate_settlement_id(cls, settlement_id, info):
        if not settlement_id:
            raise ValueError("settlement_id is required")
        return settlement_id

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, amount, info):
        if amount <= 0:
            raise ValueError("amount must be positive")
        return amount

    @field_validator("reason")
    @classmethod
    def validate_reason(cls, reason, info):
        if not reason:
            raise ValueError("reason cannot be empty")
        return reason


class WorkSettlement(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    worklog_id: UUID = Field(foreign_key="worklog.id")

    total_hours: float
    payable_hours: float
    rate_per_hour: Decimal

    gross_amount: Decimal

    settled_month: date
    status: str  # PENDING / APPROVED / PAID

    created_at: date = Field(default_factory=date.today)


class WorkPayment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    settlement_id: UUID = Field(foreign_key="worksettlement.id")

    paid_hours: float
    paid_amount: Decimal

    paid_at: datetime
    reference_id: str


class RemittanceStatus(str, Enum):
    PENDING = "PENDING"
    REMITTED = "REMITTED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Remittance(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    period_start: datetime
    period_end: datetime
    total_amount: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    status: RemittanceStatus
    created_at: date = Field(default_factory=date.today)


class RemittanceLine(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    remittance_id: UUID = Field(foreign_key="remittance.id")
    worklog_id: UUID = Field(foreign_key="timelog.id")
    amount: Decimal


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    employee_id: str = Field(max_length=3, unique=True)
