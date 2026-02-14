from sqlalchemy.exc import IntegrityError
from app.application.services.task_service import TaskService
from app.domain.schema import TaskData
from app.domain.exceptions import DuplicateTaskName
from unittest.mock import Mock
import pytest


def test_create_task_duplicate():
    repo = Mock()
    repo.create.side_effect = IntegrityError(None, None, None)
    repo.session.rollback = Mock()
    service = TaskService(repo)

    with pytest.raises(DuplicateTaskName):
        task = TaskData(name="Pranav")
        service.create_task(task)

    repo.session.rollback.assert_called_once()
