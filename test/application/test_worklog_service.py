from datetime import date
from unittest.mock import Mock

import pytest
from sqlalchemy.exc import IntegrityError

from app.application.services.worklog_service import WorkLogService
from app.domain.exceptions import WorkLogAlreadyExists, WorkLogDateRequired


def test_create_worklog_success():
    repo = Mock()
    repo.create_worklog_for_month.return_value = "worklog"
    service = WorkLogService(repo)

    result = service.create_worklog("user-id", "task-id", date(2024, 12, 5))

    assert result == "worklog"
    repo.create_worklog_for_month.assert_called_once_with(
        "user-id", "task-id", date(2024, 12, 5)
    )


def test_create_worklog_missing_user():
    repo = Mock()
    service = WorkLogService(repo)

    with pytest.raises(WorkLogDateRequired):
        service.create_worklog("", "task-id")

    repo.create_worklog_for_month.assert_not_called()


def test_create_worklog_missing_task():
    repo = Mock()
    service = WorkLogService(repo)

    with pytest.raises(WorkLogDateRequired):
        service.create_worklog("user-id", None)

    repo.create_worklog_for_month.assert_not_called()


def test_create_worklog_duplicate_rolls_back_and_raises():
    repo = Mock()
    repo.session = Mock()
    repo.create_worklog_for_month.side_effect = IntegrityError(
        None, None, None)
    service = WorkLogService(repo)

    with pytest.raises(WorkLogAlreadyExists):
        service.create_worklog("user-id", "task-id")

    repo.session.rollback.assert_called_once()
