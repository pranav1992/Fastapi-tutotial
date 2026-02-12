from fastapi import APIRouter
from ...domain.schema import UserData
from sqlmodel import Session
from fastapi import Depends
from ...infrastructure.db.session import get_session
from ...infrastructure.db.repositories.user_repo import UserRepository
from ...application.user_service import UserService
from app.domain.schema import WorkLogDataResponse


router = APIRouter(prefix="/users")


@router.post("/")
async def create_user(user: UserData, session: Session = Depends(get_session)):
    repo = UserRepository(session)
    service = UserService(repo)
    return service.create_user(user)
