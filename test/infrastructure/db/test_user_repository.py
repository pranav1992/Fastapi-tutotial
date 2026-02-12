import pytest
from sqlalchemy.exc import IntegrityError

from app.infrastructure.db.models import User
from app.infrastructure.db.repositories.user_repo import UserRepository


def test_user_repository_unique_employee_id(session):
    repo = UserRepository(session)

    repo.create(User(name="A", employee_id="1"))

    with pytest.raises(IntegrityError):
        repo.create(User(name="B", employee_id="1"))
    session.rollback()
