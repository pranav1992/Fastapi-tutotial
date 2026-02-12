from ..infrastructure.db.repositories.user_repo import UserRepository
from ..domain.schema import UserData
from sqlalchemy.exc import IntegrityError
from ..domain.exceptions import DuplicateEmployeeID, InvalidUserData


class UserService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, user: UserData):
        if not user.name:
            raise InvalidUserData("Name cannot be empty")
        if not user.employee_id:
            raise InvalidUserData("Employee ID is required")
        try:
            return self.repo.create(user)
        except IntegrityError:
            self.repo.session.rollback()
            raise DuplicateEmployeeID(user.employee_id)
