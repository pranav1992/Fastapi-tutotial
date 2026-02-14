import pytest
from unittest.mock import Mock
from sqlalchemy.exc import IntegrityError

from app.application.services.user_service import UserService
from app.domain.exceptions import DuplicateEmployeeID
from app.domain.schema import UserData


def test_create_user_duplicate_employee_id():
    # mock repository
    repo = Mock()
    repo.create.side_effect = IntegrityError(None, None, None)
    repo.session.rollback = Mock()

    service = UserService(repo)

    with pytest.raises(DuplicateEmployeeID):
        user = UserData(name="Pranav", employee_id="123")
        service.create_user(user)

    repo.session.rollback.assert_called_once()
