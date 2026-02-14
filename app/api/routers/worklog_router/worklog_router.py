from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.domain.schema import WorkLogData, WorkLogDataResponse
from app.infrastructure.db.session import get_session
from app.infrastructure.db.repositories.worklog_repo import WorkLogRepository
from app.application.services.worklog_service import WorkLogService


router = APIRouter(prefix="/worklogs")


@router.post("/", response_model=WorkLogDataResponse)
async def create_worklog(worklog: WorkLogData, 
                         session: Session = Depends(get_session)):
    repo = WorkLogRepository(session)
    service = WorkLogService(repo)
    return service.create_worklog(worklog.user_id, worklog.task_id,
                                  worklog.target_date)
