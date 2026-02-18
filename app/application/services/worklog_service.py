
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from sqlmodel import select
from fastapi import HTTPException

from app.domain.exceptions import WorkLogAlreadyExists, WorkLogDateRequired
from app.infrastructure.db.repositories.worklog_repo import WorkLogRepository
from app.domain.schema import WorkLogCreate, WorkLogQuery
from app.infrastructure.db.models import TimeLog


class WorkLogService:
    def __init__(self, repo: WorkLogRepository):
        self.repo = repo

    def create_worklog(self, worklog: WorkLogCreate):
        try:
            if not worklog.user_id:
                raise WorkLogDateRequired("user_id is required")
            if not worklog.task_id:
                raise WorkLogDateRequired("task_id is required")
            return self.repo.create_worklog(worklog)
        except IntegrityError:
            self.repo.session.rollback()
            raise WorkLogAlreadyExists("Worklog already exists")

    def get_all_worklogs(self):
        return self.repo.get_all_worklogs()

    def get_worklog(self, worklog: WorkLogQuery):
        return self.repo.get_worklog(worklog)

    def get_worklog_by_user_id(self, user_id):
        return self.repo.get_worklogs_by_user_id(user_id)

    def get_worklog_by_task_id(self, task_id):
        return self.repo.get_worklog_by_task_id(task_id)

    def ensure_worklog_exists(self, worklog: WorkLogQuery):
        return self.repo.ensure_worklog_exists(worklog)

    def list_worklogs_with_amount(
            self, remittance_status: str | None, rate_per_hour):
        if remittance_status:
            remittance_status = remittance_status.upper()
            if remittance_status not in {"REMITTED", "UNREMITTED"}:
                raise HTTPException(
                    status_code=400,
                    detail="remittanceStatus must be either REMITTED "
                    "or UNREMITTED",
                )

        # Currently uses flat rate; could be extended to per-user/task rate
        worklogs = self.repo.list_worklogs_with_remittance_status()

        # Build response with computed hours/amount
        result = []
        for wl in worklogs:
            status = "REMITTED" if wl.remittance_id else "UNREMITTED"
            if remittance_status and status != remittance_status:
                continue

            # sum hours from timelogs
            hours = 0
            for tl in self.repo.session.exec(
                select(TimeLog).where(TimeLog.worklog_id == wl.id)
            ).all():
                if tl.total_time:
                    hours += tl.total_time.total_seconds() / 3600

            amount = Decimal(hours) * Decimal(rate_per_hour)
            result.append({
                "id": wl.id,
                "user_id": wl.user_id,
                "task_id": wl.task_id,
                "task_assignment_id": wl.task_assignment_id,
                "year": wl.year,
                "month": wl.month,
                "created_at": wl.created_at,
                "remittance_status": status,
                "total_hours": hours,
                "amount": amount,
            })

        return result
