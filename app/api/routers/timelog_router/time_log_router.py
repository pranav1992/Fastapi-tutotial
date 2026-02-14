from fastapi import APIRouter, Depends
from app.application.facade.time_log_facade import TimeLogFacade
from app.api.dependency.timelog_dependencies import get_timelog_facade
from app.domain.schema import TimeLogData

router = APIRouter(prefix="/time-log")


@router.post("")
def create_timelog(
    payload: TimeLogData,
    facade: TimeLogFacade = Depends(get_timelog_facade),
):
    return facade.create_timelog(payload)
