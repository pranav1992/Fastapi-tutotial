from uuid import UUID
from typing import Union
from ..models import TaskAssignment
from sqlmodel import select
from app.domain.schema import TaskAssignmentCreate


class TaskAssignmentRepository:
    def __init__(self, session):
        self.session = session

    def create_task_assignment_to_user(self, data: TaskAssignmentCreate):
        orm = TaskAssignment(user_id=data.user_id, task_id=data.task_id)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm

    def get_tasks_assigned_by_task_assignment_id(
            self, task_assignment_id: Union[UUID, str]):
        return self.session.exec(
            select(TaskAssignment).where(
                TaskAssignment.id == task_assignment_id)
        ).first()

    def ensure_task_assigned(
            self, user_id: Union[UUID, str], task_id: Union[UUID, str]):
        return self.session.exec(
            select(TaskAssignment).where(
                TaskAssignment.user_id == user_id,
                TaskAssignment.task_id == task_id)
        ).first()

    def get_tasks_assigned_by_user_id(self, user_id: Union[UUID, str]):
        return self.session.exec(
            select(TaskAssignment).where(
                TaskAssignment.user_id == user_id)
        ).all()

    def get_tasks_assigned_by_task_id(self, task_id: Union[UUID, str]):
        return self.session.exec(
            select(TaskAssignment).where(
                TaskAssignment.task_id == task_id)
        ).all()

    def get_all_tasks_assigned(self):
        return self.session.exec(select(TaskAssignment)).all()
