from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.domain.schema import RemittancePayRequest, RemittanceRead
from app.infrastructure.db.session import get_session
from app.infrastructure.db.repositories.remittance_repo import\
                                                 RemittanceRepository
from app.application.services.remittance_service import RemittanceService

router = APIRouter(prefix="/remittances")


@router.post("/pay-month/", response_model=RemittanceRead)
def pay_month(payload: RemittancePayRequest, session: Session = 
              Depends(get_session)):
    repo = RemittanceRepository(session)
    service = RemittanceService(repo)
    return service.pay_month(payload)
