from fastapi import Depends
from sqlmodel import Session

from app.infrastructure.db.session import get_session
from app.infrastructure.db.repositories.time_log_repository import\
      TimeLogRepository
from app.infrastructure.db.repositories.task_assignment_repo import\
                                                    TaskAssignmentRepository
from app.infrastructure.db.repositories.worklog_repo import WorkLogRepository
# from app.infrastructure.db.repositories.settlement_repo
# import SettlementRepository

from app.application.services.time_log_service import TimeLogService
from app.application.services.task_assignment_service import\
                                                    TaskAssignmentService
from app.application.services.worklog_service import WorkLogService
# from app.application.services.settlement_service import SettlementService

from app.application.facade.time_log_facade import TimeLogFacade


def get_timelog_facade(
    session: Session = Depends(get_session),
) -> TimeLogFacade:
    timelog_repo = TimeLogRepository(session)
    assignment_repo = TaskAssignmentRepository(session)
    worklog_repo = WorkLogRepository(session)
    # settlement_repo = SettlementRepository(session)

    timelog_service = TimeLogService(timelog_repo)
    assignment_service = TaskAssignmentService(assignment_repo)
    worklog_service = WorkLogService(worklog_repo)
    # settlement_service = SettlementService(settlement_repo)

    return TimeLogFacade(
        timelog_service=timelog_service,
        assignment_service=assignment_service,
        worklog_service=worklog_service,
        # settlement_service=settlement_service,
        session=session,
    )
