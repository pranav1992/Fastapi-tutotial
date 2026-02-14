from fastapi import APIRouter
from app.domain.schema import UserData
from sqlmodel import Session
from fastapi import Depends
from app.infrastructure.db.session import get_session
from app.infrastructure.db.repositories.user_repo import UserRepository
from app.application.services.user_service import UserService


router = APIRouter(prefix="/users")


@router.post("/create-user/")
async def create_user(user: UserData, session: Session = Depends(get_session)):
    repo = UserRepository(session)
    service = UserService(repo)
    return service.create_user(user)


@router.get("/get-all-users/")
async def get_all_users(session: Session = Depends(get_session)):
    repo = UserRepository(session)
    service = UserService(repo)
    return service.get_all_users()
