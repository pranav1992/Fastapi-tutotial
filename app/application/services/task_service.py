
from app.infrastructure.db.repositories.task_repo import TaskRepository
from app.domain.schema import TaskData
from app.domain.exceptions import (
    DuplicateTaskName, TaskNameRequired, TaskNameLengthExceeded)
from sqlalchemy.exc import IntegrityError


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, task: TaskData):
        try:
            if not task.name:
                raise TaskNameRequired("Task name cannot be empty")

            if len(task.name) > 200:
                raise TaskNameLengthExceeded(task.name, "200")

            return self.repo.create(task)
        except IntegrityError:
            self.repo.session.rollback()
            raise DuplicateTaskName(task.name)

    def get_all_tasks(self):
        return self.repo.get_all_tasks()
