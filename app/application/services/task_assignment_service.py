from sqlalchemy.exc import IntegrityError
from app.domain.exceptions import InvalidTaskAssignment, TaskAlreadyAssigned
from app.infrastructure.db.repositories.task_assignment_repo import\
                                                    TaskAssignmentRepository
from app.domain.schema import TaskAssignmentCreate
from typing import Union
from uuid import UUID


class TaskAssignmentService:
    def __init__(self, repo: TaskAssignmentRepository):
        self.repo = repo

    def create_task_assignment(self, data: TaskAssignmentCreate):
        if not data.user_id:
            raise InvalidTaskAssignment("user_id is required")

        if not data.task_id:
            raise InvalidTaskAssignment("task_id is required")

        try:
            return self.repo.create_task_assignment_to_user(data)

        except IntegrityError:
            self.repo.session.rollback()
            raise TaskAlreadyAssigned(str(data.user_id), str(data.task_id))

        except Exception as e:
            self.repo.session.rollback()
            raise e

    def get_task_assignment_by_id(self, assigned_task_id: Union[UUID, str]):
        return self.repo.get_tasks_assigned_by_task_assignment_id(
                                                        assigned_task_id)

    def ensure_task_assigned(self, user_id: Union[UUID, str],
                             task_id: Union[UUID, str]):
        return self.repo.ensure_task_assigned(user_id, task_id)

    def get_task_assignments_by_user_id(self, user_id: Union[UUID, str]):
        return self.repo.get_tasks_assigned_by_user_id(user_id)

    def get_task_assignments_by_task_id(self, task_id: Union[UUID, str]):
        return self.repo.get_tasks_assigned_by_task_id(task_id)

    def get_all_task_assignments(self):
        return self.repo.get_all_tasks_assigned()
