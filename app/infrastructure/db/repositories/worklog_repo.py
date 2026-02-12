from typing import Union, Optional
from uuid import UUID
from datetime import date
from app.infrastructure.db.models import WorkLog
from sqlmodel import select


class WorkLogRepository:
    def __init__(self, session):
        self.session = session

    def create_worklog_for_month(
              self, user_id: Union[UUID, str],
              task_id: Union[UUID, str], target_date: Optional[date] = None):
        current = target_date or date.today()
        user_uuid = UUID(str(user_id))
        task_uuid = UUID(str(task_id))

        worklog = WorkLog(
            user_id=user_uuid,
            task_id=task_uuid,
            year=current.year,
            month=current.month,
        )
        # Avoid duplicate worklogs for the same user/task/month
        existing = self.session.exec(
            select(WorkLog).where(
                WorkLog.user_id == user_uuid,
                WorkLog.task_id == task_uuid,
                WorkLog.year == current.year,
                WorkLog.month == current.month,
            )
        ).first()
        if existing:
            return existing

        self.session.add(worklog)
        self.session.commit()
        self.session.refresh(worklog)
        return worklog
