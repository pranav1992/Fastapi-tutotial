from fastapi import APIRouter, Depends
from app.application.facade.time_log_facade import TimeLogFacade
from app.api.dependency.timelog_dependencies import get_timelog_facade
from app.domain.schema import TimeLogCreate, TimeLogRead

router = APIRouter(prefix="/time-log")


@router.post("/create-time-log/", response_model=TimeLogRead)
def create_timelog(
    payload: TimeLogCreate,
    facade: TimeLogFacade = Depends(get_timelog_facade),
):
    return facade.create_timelog(payload)


@router.get("/get-all-time-logs/", response_model=list[TimeLogRead])
def get_all_timelogs(facade: TimeLogFacade = Depends(get_timelog_facade)):
    return facade.get_all_timelogs()
