from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.application.services.task_assignment_service\
                                            import TaskAssignmentService
from app.domain.schema import TaskAssignmentCreate
from app.domain.exceptions import InvalidTaskAssignment, TaskAlreadyAssigned


def test_create_task_assignment_success():
    repo = Mock()
    repo.create_task_assignment_to_user.return_value = "assignment"
    service = TaskAssignmentService(repo)

    payload = TaskAssignmentCreate(
        user_id="11111111-1111-1111-1111-111111111111",
        task_id="22222222-2222-2222-2222-222222222222",
    )
    result = service.create_task_assignment(payload)

    assert result == "assignment"
    repo.create_task_assignment_to_user.assert_called_once_with(payload)


def test_create_task_assignment_missing_user():
    repo = Mock()
    service = TaskAssignmentService(repo)

    with pytest.raises(Exception):  # ValidationError from Pydantic
        TaskAssignmentCreate(user_id=None, task_id="22222222-2222-2222-2222-222222222222")

    repo.create_task_assignment_to_user.assert_not_called()


def test_create_task_assignment_missing_task():
    repo = Mock()
    service = TaskAssignmentService(repo)

    with pytest.raises(Exception):  # ValidationError from Pydantic
        TaskAssignmentCreate(user_id="11111111-1111-1111-1111-111111111111", task_id=None)

    repo.create_task_assignment_to_user.assert_not_called()


def test_create_task_assignment_duplicate():
    repo = Mock()
    repo.session = Mock()
    repo.create_task_assignment_to_user.side_effect = IntegrityError(
        None, None, None)
    service = TaskAssignmentService(repo)

    payload = TaskAssignmentCreate(
        user_id="11111111-1111-1111-1111-111111111111",
        task_id="22222222-2222-2222-2222-222222222222",
    )
    with pytest.raises(TaskAlreadyAssigned):
        service.create_task_assignment(payload)

    repo.session.rollback.assert_called_once()

    repo.create_task_assignment_to_user.assert_called_once()
