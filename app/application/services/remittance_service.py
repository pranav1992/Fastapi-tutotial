from decimal import Decimal
from fastapi import HTTPException

from app.domain.schema import RemittancePayRequest
from app.infrastructure.db.repositories.remittance_repo import\
                                             RemittanceRepository


class RemittanceService:
    def __init__(self, repo: RemittanceRepository):
        self.repo = repo

    def pay_month(self, payload: RemittancePayRequest):
        try:
            return self.repo.pay_month(
                user_id=payload.user_id,
                year=payload.year,
                month=payload.month,
                rate_per_hour=Decimal(payload.rate_per_hour),
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            # bubble up unexpected errors
            raise
