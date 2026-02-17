from app.application.services.task_assignment_service import\
                                            TaskAssignmentService
from app.application.services.time_log_service import TimeLogService
from app.application.services.worklog_service import WorkLogService
from app.domain.exceptions import TaskNotFound, WorkLogNotFound
from app.domain.schema import TimeLogCreate, WorkLogQuery


class TimeLogFacade:
    def __init__(
        self,
        timelog_service: TimeLogService,
        assignment_service: TaskAssignmentService,
        worklog_service: WorkLogService,

        session,
    ):
        self.timelog_service = timelog_service
        self.assignment_service = assignment_service
        self.worklog_service = worklog_service
        self.session = session

    def check_task_assignment(self, task_assignment_id):
        assignment = self.assignment_service.get_task_assignment_by_id(
            task_assignment_id)
        if not assignment:
            raise TaskNotFound(task_assignment_id)
        return assignment

    def check_worklog(self, data: TimeLogCreate):
        worklog = self.worklog_service.ensure_worklog_exists(
            WorkLogQuery(
                user_id=data.user_id,
                task_id=data.task_id,
                task_assignment_id=data.task_assignment_id,
                year=data.start_time.year,
                month=data.start_time.month
            )
        )
        if not worklog:
            raise WorkLogNotFound("Worklog not found")
        return worklog

    def create_timelog(self, data: TimeLogCreate):
        try:
            assignment = self.check_task_assignment(data.task_assignment_id)
            if not assignment:
                return None
            worklog = self.check_worklog(data)
            if not worklog:
                return None
            timelog = self.timelog_service.create_time_log(data, worklog.id)
            return timelog
        except Exception:
            self.session.rollback()
            raise

    def get_all_timelogs(self):
        return self.timelog_service.get_all_time_logs()
