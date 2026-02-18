from decimal import Decimal
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.domain.schema import (
    WorkLogCreate, WorkLogRead, WorkLogQuery, WorkLogAmountRead)
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


@router.get("/list-all-worklogs", response_model=list[WorkLogAmountRead])
async def list_all_worklogs(
        remittanceStatus: str | None = None,
        rate_per_hour: Decimal = Decimal("1"),
        session: Session = Depends(get_session)):
    repo = WorkLogRepository(session)
    service = WorkLogService(repo)
    return service.list_worklogs_with_amount(remittanceStatus, rate_per_hour)
