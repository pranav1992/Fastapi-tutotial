from sqlalchemy.exc import IntegrityError
from app.domain.exceptions import InvalidTaskAssignment, TaskAlreadyAssigned


class TaskAssignmentService:
    def __init__(self, repo):
        self.repo = repo

    def create_task_assignment(self, user_id, task_id):
        # 1️ Validate input (business invariant)
        if not user_id:
            raise InvalidTaskAssignment("user_id is required")

        if not task_id:
            raise InvalidTaskAssignment("task_id is required")

        # 2️ Try assignment
        try:
            return self.repo.task_assignment_to_user(user_id, task_id)

        # 3️Translate DB constraint → domain error
        except IntegrityError:
            self.repo.session.rollback()
            raise TaskAlreadyAssigned(user_id, task_id)

    def create_worklog(self, user_id, task_id, target_date=None):
        if not user_id:
            raise InvalidTaskAssignment("user_id is required")

        if not task_id:
            raise InvalidTaskAssignment("task_id is required")

        return self.repo.create_worklog_for_month(user_id,
                                                  task_id, target_date)
