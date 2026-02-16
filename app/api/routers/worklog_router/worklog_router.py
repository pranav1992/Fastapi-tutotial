from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.domain.schema import WorkLogCreate, WorkLogRead, WorkLogQuery
from app.infrastructure.db.session import get_session
from app.infrastructure.db.repositories.worklog_repo import WorkLogRepository
from app.application.services.worklog_service import WorkLogService


router = APIRouter(prefix="/worklogs")


@router.post("/create-worklog/", response_model=WorkLogRead)
async def create_worklog(
        worklog: WorkLogCreate, session: Session = Depends(get_session)):
    repo = WorkLogRepository(session)
    service = WorkLogService(repo)
    return service.create_worklog(worklog)


@router.get("/get-all-worklogs/", response_model=list[WorkLogRead])
async def get_all_worklogs(session: Session = Depends(get_session)):
    repo = WorkLogRepository(session)
    service = WorkLogService(repo)
    return service.get_all_worklogs()


@router.get("/get-worklog/", response_model=WorkLogRead)
async def get_worklog(
        worklog: WorkLogQuery, session: Session = Depends(get_session)):
    repo = WorkLogRepository(session)
    service = WorkLogService(repo)
    return service.get_worklog(worklog)


@router.get("/get-worklog-by-user-id/", response_model=list[WorkLogRead])
async def get_worklog_by_user_id(
        user_id: str, session: Session = Depends(get_session)):
    repo = WorkLogRepository(session)
    service = WorkLogService(repo)
    return service.get_worklog_by_user_id(user_id)


@router.get("/get-worklog-by-task-id/", response_model=list[WorkLogRead])
async def get_worklog_by_task_id(
        task_id: str, session: Session = Depends(get_session)):
    repo = WorkLogRepository(session)
    service = WorkLogService(repo)
    return service.get_worklog_by_task_id(task_id)
