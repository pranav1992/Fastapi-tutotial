
from sqlmodel import Session, select
from app.domain.schema import TaskData
from ..models import Task
from app.domain.exceptions import TaskNotFound


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, task: TaskData):
        orm = Task(
            name=task.name,
            name_lower=task.name.lower(),
            description=task.description
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm

    def get_task_by_name(self, task: TaskData):
        task = Task.select().where(Task.name_lower == task.lower_name).first()
        if not task:
            raise TaskNotFound(task.lower_name)
        return task

    def get_all_tasks(self):
        return self.session.exec(select(Task)).all()
