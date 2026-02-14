from app.domain.schema import TimeLogData
from app.infrastructure.db.repositories.time_log_repository import\
      TimeLogRepository


class TimeLogService:
    def __init__(self, repo: TimeLogRepository):
        self.repo = repo

    def create_time_log(self, time_log: TimeLogData):
        try:
            if not time_log.start_time:
                raise ValueError("Start time cant be emptied")
            if not time_log.end_time:
                raise ValueError("End time cant be emptied")
            if not time_log.task_id:
                raise ValueError("Task id cant be emptied")
            if not time_log.user_id:
                raise ValueError("User id cant be emptied")
            return self.repo.create_time_log(time_log)
        except Exception as e:
            raise e
