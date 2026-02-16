
from sqlalchemy.exc import IntegrityError
from app.domain.exceptions import WorkLogAlreadyExists, WorkLogDateRequired
from app.infrastructure.db.repositories.worklog_repo import WorkLogRepository
from app.domain.schema import WorkLogCreate, WorkLogQuery


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
