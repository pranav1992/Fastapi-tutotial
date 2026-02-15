from datetime import date
from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from app.domain.exceptions import WorkLogAlreadyExists, WorkLogDateRequired
from app.infrastructure.db.repositories.worklog_repo import WorkLogRepository
from app.infrastructure.db.models import WorkLog


class WorkLogService:
    def __init__(self, repo: WorkLogRepository):
        self.repo = repo

    def create_worklog(self, user_id, task_id,
                       target_date: Optional[date] = None):
        try:
            if not user_id:
                raise WorkLogDateRequired("user_id is required")
            if not task_id:
                raise WorkLogDateRequired("task_id is required")
            return self.repo.create_worklog_for_month(
                user_id, task_id, target_date)
        except IntegrityError:
            self.repo.session.rollback()
            raise WorkLogAlreadyExists("Worklog already exists")

    def get_worklog_for_month(self, user_id, task_id, year, month):
        return self.repo.get_worklog(user_id, task_id, year, month)

    def get_all_worklogs(self):
        return self.repo.session.exec(select(WorkLog)).all()
