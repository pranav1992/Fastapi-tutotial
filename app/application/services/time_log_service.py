from fastapi import HTTPException
from app.domain.schema import TimeLogCreate
from app.infrastructure.db.repositories.time_log_repository import\
      TimeLogRepository


class TimeLogService:
    def __init__(self, repo: TimeLogRepository):
        self.repo = repo

    def create_time_log(self, time_log: TimeLogCreate):
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
        except ValueError as e:
            # Convert domain validation errors to a 400 response for clients
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            # Let unexpected errors bubble up as 500s
            raise

    def get_all_time_logs(self):
        return self.repo.get_all_time_logs()
