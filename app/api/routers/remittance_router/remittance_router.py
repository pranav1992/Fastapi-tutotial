from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.domain.schema import (
    RemittancePayRequest,
    RemittanceBulkPayRequest,
    RemittanceBulkPayResponse,
    RemittanceRead,
    RemittancePreview,
)
from app.infrastructure.db.session import get_session
from app.infrastructure.db.repositories.remittance_repo import\
                                                 RemittanceRepository
from app.application.services.remittance_service import RemittanceService
from app.infrastructure.db.repositories.user_repo import UserRepository

router = APIRouter(prefix="/remittances")


@router.post("/pay-month/", response_model=RemittanceRead)
def pay_month(payload: RemittancePayRequest, session: Session =
              Depends(get_session)):
    repo = RemittanceRepository(session)
    service = RemittanceService(repo)
    return service.pay_month(payload)


@router.post("/calculate-month/", response_model=RemittancePreview)
def calculate_month(payload: RemittancePayRequest, session: Session =
                    Depends(get_session)):
    repo = RemittanceRepository(session)
    service = RemittanceService(repo)
    return service.calculate_month(payload)


@router.post("/generate-remittances-for-all-users",
             response_model=RemittanceBulkPayResponse)
def generate_remittances_for_all_users(
        payload: RemittanceBulkPayRequest,
        session: Session = Depends(get_session)):
    repo = RemittanceRepository(session)
    user_repo = UserRepository(session)
    service = RemittanceService(repo, user_repo=user_repo)
    return service.generate_remittances_for_all_users(payload)
