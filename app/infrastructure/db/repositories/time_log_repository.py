from app.domain.schema import TimeLogData
from app.infrastructure.db.models import TimeLog


class TimeLogRepository:
    def __init__(self, session):
        self.session = session

    def create_time_log(self, time_log: TimeLogData):
        orm = TimeLog(
            task_id=time_log.task_id,
            user_id=time_log.user_id,
            start_time=time_log.start_time,
            end_time=time_log.end_time,
            total_time=time_log.total_time
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return time_log
