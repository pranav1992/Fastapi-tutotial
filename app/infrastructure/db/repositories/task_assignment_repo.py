from uuid import UUID
from typing import Union
from ..models import TaskAssignment
from sqlmodel import select


class TaskAssignmentRepository:
    def __init__(self, session):
        self.session = session

    def task_assignment_to_user(self, user_id: Union[UUID, str],
                                task_id: Union[UUID, str]):
        # Accept string UUIDs from callers and normalise to UUID
        # objects for SQLModel
        user_uuid = UUID(str(user_id))
        task_uuid = UUID(str(task_id))

        orm = TaskAssignment(user_id=user_uuid, task_id=task_uuid)
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm

    def get_assigned_tasks(self, assigned_task_id: Union[UUID, str]):
        return self.session.exec(
            select(TaskAssignment).where(TaskAssignment.id == assigned_task_id)
        ).first()

    def get_assignment_for_user_task(
        self, user_id: Union[UUID, str], task_id: Union[UUID, str],
        active_only: bool = True
    ):
        """Fetch a task assignment for a given user and task."""
        conditions = [
            TaskAssignment.user_id == user_id,
            TaskAssignment.task_id == task_id,
        ]
        if active_only:
            conditions.append(TaskAssignment.active.is_(True))

        return self.session.exec(select(TaskAssignment).
                                 where(*conditions)).first()

    def get_all_task_assignments(self):
        return self.session.exec(select(TaskAssignment)).all()
