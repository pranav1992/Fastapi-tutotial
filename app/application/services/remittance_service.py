from decimal import Decimal
from fastapi import HTTPException

from app.domain.schema import (
    RemittancePayRequest,
    RemittanceBulkPayRequest,
    RemittanceBulkPayResponse,
    RemittancePreview,
    RemittanceWorklogBreakdown,
)
from app.infrastructure.db.repositories.remittance_repo import\
                                            RemittanceRepository
from app.infrastructure.db.repositories.user_repo import UserRepository


class RemittanceService:
    def __init__(
            self, repo: RemittanceRepository,
            user_repo: UserRepository | None = None):
        self.repo = repo
        self.user_repo = user_repo

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

    def generate_remittances_for_all_users(
            self,
            payload: RemittanceBulkPayRequest) -> RemittanceBulkPayResponse:
        if not self.user_repo:
            raise HTTPException(
                status_code=500, detail="User repository not configured")

        remittances = []
        errors = {}

        for user in self.user_repo.get_all_users():
            try:
                remittance = self.repo.pay_month(
                    user_id=user.id,
                    year=payload.year,
                    month=payload.month,
                    rate_per_hour=Decimal(payload.rate_per_hour),
                )
                remittances.append(remittance)
            except ValueError as e:
                errors[str(user.id)] = str(e)
            except Exception as e:
                errors[str(user.id)] = f"Unexpected error: {e}"

        return RemittanceBulkPayResponse(
            remittances=remittances, errors=errors)

    def calculate_month(
            self, payload: RemittancePayRequest) -> RemittancePreview:
        try:
            total_hours, payable_hours, total_amount, breakdown_map =\
                self.repo.calculate_month(
                    user_id=payload.user_id,
                    year=payload.year,
                    month=payload.month,
                    rate_per_hour=Decimal(payload.rate_per_hour),
                )

            breakdown = [
                RemittanceWorklogBreakdown(
                    worklog_id=wl_id,
                    hours=hours,
                    amount=Decimal(hours) * Decimal(payload.rate_per_hour),
                )
                for wl_id, hours in breakdown_map.items()
            ]

            return RemittancePreview(
                user_id=payload.user_id,
                year=payload.year,
                month=payload.month,
                total_hours=total_hours,
                payable_hours=payable_hours,
                rate_per_hour=Decimal(payload.rate_per_hour),
                total_amount=total_amount,
                breakdown=breakdown,
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception:
            raise
