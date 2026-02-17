from datetime import timedelta

from app.domain.schema import TimeLogCreate
from app.infrastructure.db.models import TimeLog
from sqlmodel import select


class TimeLogRepository:
    def __init__(self, session):
        self.session = session

    def create_time_log(self, time_log: TimeLogCreate, worklog_id):
        # Compute and validate duration before persisting
        duration = time_log.end_time - time_log.start_time
        if duration <= timedelta(0):
            raise ValueError("end_time must be after start_time")
        if duration > timedelta(hours=12):
            raise ValueError("timelog duration cannot exceed 12 hours")

        orm = TimeLog(
            task_id=time_log.task_id,
            user_id=time_log.user_id,
            task_assignment_id=time_log.task_assignment_id,
            worklog_id=worklog_id,
            start_time=time_log.start_time,
            end_time=time_log.end_time,
            total_time=duration,
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm

    def get_all_time_logs(self):
        return self.session.exec(select(TimeLog)).all()

    def get_time_log_by_id(self, id: str):
        return self.session.exec(select(TimeLog).
                                 where(TimeLog.id == id)).first()
