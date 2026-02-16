
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.application.services.worklog_service import WorkLogService
from app.domain.exceptions import WorkLogAlreadyExists
from app.domain.schema import WorkLogCreate


def test_create_worklog_success():
    repo = Mock()
    repo.create_worklog.return_value = "worklog"
    service = WorkLogService(repo)

    payload = WorkLogCreate(
        user_id="11111111-1111-1111-1111-111111111111",
        task_id="22222222-2222-2222-2222-222222222222",
        task_assignment_id="22222222-2222-2222-2222-222222222222",
        year=2024,
        month=12,
    )
    result = service.create_worklog(payload)

    assert result == "worklog"
    repo.create_worklog.assert_called_once_with(payload)


def test_create_worklog_missing_user():
    repo = Mock()

    with pytest.raises(Exception):  # ValidationError from Pydantic
        WorkLogCreate(
            user_id=None,
            task_id="22222222-2222-2222-2222-222222222222",
            task_assignment_id="22222222-2222-2222-2222-222222222222",
            year=2024, month=12)

    repo.create_worklog.assert_not_called()


def test_create_worklog_missing_task():
    repo = Mock()

    with pytest.raises(Exception):
        WorkLogCreate(
            user_id="11111111-1111-1111-1111-111111111111",
            task_id=None,
            task_assignment_id=None,
            year=2024, month=12)

    repo.create_worklog.assert_not_called()


def test_create_worklog_duplicate_rolls_back_and_raises():
    repo = Mock()
    repo.session = Mock()
    repo.create_worklog.side_effect = IntegrityError(None, None, None)
    service = WorkLogService(repo)

    payload = WorkLogCreate(
        user_id="11111111-1111-1111-1111-111111111111",
        task_id="22222222-2222-2222-2222-222222222222",
        task_assignment_id="22222222-2222-2222-2222-222222222222",
        year=2024, month=12)
    with pytest.raises(WorkLogAlreadyExists):
        service.create_worklog(payload)

    repo.session.rollback.assert_called_once()
