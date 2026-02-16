from app.application.services.task_assignment_service import\
                                            TaskAssignmentService
from app.application.services.time_log_service import TimeLogService
from app.application.services.worklog_service import WorkLogService
from app.domain.exceptions import TaskNotFound, WorkLogNotFound
from app.domain.schema import TimeLogCreate


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

    def check_task_assignment(self, user_id, task_id):
        assignment = self.assignment_service.ensure_active(user_id, task_id)
        if not assignment:
            raise TaskNotFound(task_id)
        return assignment

    def check_worklog(self, user_id, task_id, year, month):
        worklog = self.worklog_service.get_worklog_for_month(
            user_id, task_id, year, month
        )
        if not worklog:
            raise WorkLogNotFound("Worklog not found")
        return worklog

    def create_timelog(self, data: TimeLogCreate):
        try:
            print(data)

            # assignment = self.check_task_assignment(
            # data.user_id, data.task_id)
            # if not assignment:
            #     return None
            # worklog = self.check_worklog(
            #     data.user_id, data.task_id, data.year, data.month
            # )
            # if not worklog:
            #     # create a worklog
            #     self.worklog_service.create_worklog(
            #         data.user_id, data.task_id, data.created_at)
            timelog = self.timelog_service.create_time_log(data)
            return timelog

        except Exception:
            self.session.rollback()
            raise

    def get_all_timelogs(self):
        return self.timelog_service.get_all_time_logs()
