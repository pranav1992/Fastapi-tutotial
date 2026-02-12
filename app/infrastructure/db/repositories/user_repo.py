
from sqlmodel import Session
from app.domain.schema import UserData
from ..models import User


class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def create(self, userData: UserData) -> UserData:
        orm = User(
            name=userData.name,
            employee_id=userData.employee_id
        )
        self.session.add(orm)
        self.session.commit()
        self.session.refresh(orm)
        return orm
