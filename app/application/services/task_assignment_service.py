from sqlalchemy.exc import IntegrityError
from app.domain.exceptions import InvalidTaskAssignment, TaskAlreadyAssigned
from app.infrastructure.db.repositories.task_assignment_repo import\
                                                    TaskAssignmentRepository
from typing import Union
from uuid import UUID


class TaskAssignmentService:
    def __init__(self, repo: TaskAssignmentRepository):
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

        # 4️ Unexpected error
        except Exception as e:
            self.repo.session.rollback()
            raise e

    def get_assigned_tasks_by_id(self, assigned_task_id: Union[UUID, str]):
        return self.repo.get_assigned_tasks(assigned_task_id)

    def ensure_active(self, user_id: Union[UUID, str],
                      task_id: Union[UUID, str]):
        """Return an active assignment for the user-task pair or ``None``."""
        return self.repo.get_assignment_for_user_task(user_id, task_id)

    def get_all_task_assignments(self):
        return self.repo.get_all_task_assignments()
