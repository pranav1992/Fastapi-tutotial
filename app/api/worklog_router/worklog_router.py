from fastapi import APIRouter, Depends
from sqlmodel import Session

from ...domain.schema import WorkLogData, WorkLogDataResponse
from ...infrastructure.db.session import get_session
from ...infrastructure.db.repositories.worklog_repo import WorkLogRepository
from ...application.worklog_service import WorkLogService


router = APIRouter(prefix="/worklogs")


@router.post("/", response_model=WorkLogDataResponse)
async def create_worklog(worklog: WorkLogData, session: Session = Depends(get_session)):
    repo = WorkLogRepository(session)
    service = WorkLogService(repo)
    return service.create_worklog(worklog.user_id, worklog.task_id, worklog.target_date)
