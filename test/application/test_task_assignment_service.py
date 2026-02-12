from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.application.task_assignment_service import TaskAssignmentService
from app.domain.exceptions import InvalidTaskAssignment, TaskAlreadyAssigned


def test_create_task_assignment_success():
    repo = Mock()
    repo.task_assignment_to_user.return_value = "assignment"
    service = TaskAssignmentService(repo)

    result = service.create_task_assignment("user-id", "task-id")

    assert result == "assignment"
    repo.task_assignment_to_user.assert_called_once_with("user-id", "task-id")


def test_create_task_assignment_missing_user():
    repo = Mock()
    service = TaskAssignmentService(repo)

    with pytest.raises(InvalidTaskAssignment):
        service.create_task_assignment("", "task-id")

    repo.task_assignment_to_user.assert_not_called()


def test_create_task_assignment_missing_task():
    repo = Mock()
    service = TaskAssignmentService(repo)

    with pytest.raises(InvalidTaskAssignment):
        service.create_task_assignment("user-id", None)

    repo.task_assignment_to_user.assert_not_called()


def test_create_task_assignment_duplicate():
    repo = Mock()
    repo.session = Mock()
    repo.task_assignment_to_user.side_effect = IntegrityError(None, None, None)
    service = TaskAssignmentService(repo)

    with pytest.raises(TaskAlreadyAssigned):
        service.create_task_assignment("user-id", "task-id")

    repo.session.rollback.assert_called_once()


def test_create_worklog_success():
    repo = Mock()
    repo.create_worklog_for_month.return_value = "worklog"
    service = TaskAssignmentService(repo)

    result = service.create_worklog("user-id", "task-id")

    assert result == "worklog"
    repo.create_worklog_for_month.assert_called_once_with("user-id", "task-id", None)


def test_create_worklog_missing_user():
    repo = Mock()
    service = TaskAssignmentService(repo)

    with pytest.raises(InvalidTaskAssignment):
        service.create_worklog("", "task-id")

    repo.create_worklog_for_month.assert_not_called()


def test_create_worklog_missing_task():
    repo = Mock()
    service = TaskAssignmentService(repo)

    with pytest.raises(InvalidTaskAssignment):
        service.create_worklog("user-id", None)

    repo.create_worklog_for_month.assert_not_called()
