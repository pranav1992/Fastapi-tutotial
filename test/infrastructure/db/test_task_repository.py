from app.infrastructure.db.repositories.task_repo import TaskRepository
from app.domain.schema import TaskData
from sqlalchemy.exc import IntegrityError
import pytest


def test_task_repository_unique_name(session):
    repo = TaskRepository(session)

    repo.create(TaskData(name="B"))

    with pytest.raises(IntegrityError):
        repo.create(TaskData(name="B"))
    session.rollback()

    with pytest.raises(IntegrityError):
        repo.create(TaskData(name="b"))
    session.rollback()
