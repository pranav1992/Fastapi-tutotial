
from app.infrastructure.db.models import WorkLog
from sqlmodel import select
from app.domain.schema import WorkLogCreate, WorkLogQuery


class WorkLogRepository:
    def __init__(self, session):
        self.session = session

    def create_worklog(self, worklog: WorkLogCreate):
        worklog = WorkLog(
            user_id=worklog.user_id,
            task_id=worklog.task_id,
            task_assignment_id=worklog.task_assignment_id,
            year=worklog.year,
            month=worklog.month,
        )
        # Avoid duplicate worklogs for the same user/task/month
        existing = self.session.exec(
            select(WorkLog).where(
                WorkLog.user_id == worklog.user_id,
                WorkLog.task_assignment_id == worklog.task_assignment_id,
                WorkLog.year == worklog.year,
                WorkLog.month == worklog.month,
            )
        ).first()
        if existing:
            return existing

        self.session.add(worklog)
        self.session.commit()
        self.session.refresh(worklog)
        return worklog

    def get_worklog(self, worklog: WorkLogQuery):
        return self.session.exec(
            select(WorkLog).where(
                WorkLog.user_id == worklog.user_id,
                WorkLog.task_id == worklog.task_id,
                WorkLog.year == worklog.year,
                WorkLog.month == worklog.month,
            )
        ).first()

    def ensure_worklog_exists(self, worklog: WorkLogQuery):
        isExist = self.get_worklog(worklog)
        if not isExist:
            worklog = self.create_worklog(WorkLogCreate(
                user_id=worklog.user_id, task_id=worklog.task_id,
                year=worklog.year, month=worklog.month,
                task_assignment_id=worklog.task_assignment_id))
        return worklog

    def get_worklogs_by_user_id(self, user_id):
        return self.session.exec(
            select(WorkLog).where(WorkLog.user_id == user_id)
        ).all()

    def get_worklog_by_task_id(self, task_id):
        return self.session.exec(
            select(WorkLog).where(WorkLog.task_id == task_id)
        ).all()

    def get_all_worklogs(self):
        return self.session.exec(select(WorkLog)).all()
