from datetime import date, datetime
from decimal import Decimal
from typing import List

from sqlmodel import select

from app.infrastructure.db.models import (
    Remittance,
    RemittanceLine,
    RemittanceStatus,
    TimeLog,
    WorkLog,
)


class RemittanceRepository:
    def __init__(self, session):
        self.session = session

    # Public API
    def pay_month(self, user_id, year: int, month: int, rate_per_hour: Decimal):
        """
        Aggregate all worklogs + timelogs for a user/month, create a remittance,
        generate payment lines per worklog, and mark worklogs as paid.
        Idempotent: if a REMITTED record already exists for that month, return it.
        """
        month_anchor = date(year, month, 1)

        existing = self._get_remittance(user_id, month_anchor)
        if existing and existing.status == RemittanceStatus.REMITTED:
            return existing

        worklogs = self._get_worklogs(user_id, year, month)
        if not worklogs:
            raise ValueError("No worklogs found for this user and month")

        worklog_ids = [w.id for w in worklogs]
        timelogs = self._get_timelogs(worklog_ids)
        if not timelogs:
            raise ValueError("No timelogs found for this user and month")

        # Compute hours per worklog and totals
        hours_per_worklog = self._accumulate_hours_by_worklog(timelogs)
        total_hours = sum(hours_per_worklog.values())
        if total_hours <= 0:
            raise ValueError("Total hours must be positive to create remittance")

        payable_hours = total_hours  # Placeholder for future adjustments
        total_amount = (Decimal(payable_hours) * Decimal(rate_per_hour))

        # Create or reuse remittance record
        remittance = existing or Remittance(
            user_id=user_id,
            total_hours=total_hours,
            payable_hours=payable_hours,
            rate_per_hour=rate_per_hour,
            total_amount=total_amount,
            settled_month_and_year=month_anchor,
            status=RemittanceStatus.PENDING,
        )

        if existing:
            remittance.total_hours = total_hours
            remittance.payable_hours = payable_hours
            remittance.total_amount = total_amount
            remittance.status = RemittanceStatus.PENDING

        self.session.add(remittance)
        self.session.flush()  # ensure remittance.id for FK usage

        # Mark worklogs as paid and attach remittance id
        for wl in worklogs:
            wl.remittance_id = remittance.id

        # Create payment lines (one per worklog)
        for wl_id, hours in hours_per_worklog.items():
            paid_amount = Decimal(hours) * Decimal(rate_per_hour)
            line = RemittanceLine(
                remittance_id=remittance.id,
                worklog_id=wl_id,
                paid_hours=hours,
                paid_amount=paid_amount,
                paid_at=datetime.utcnow(),
            )
            self.session.add(line)

        remittance.status = RemittanceStatus.REMITTED
        self.session.commit()
        self.session.refresh(remittance)
        return remittance

    # Helpers
    def _get_remittance(self, user_id, month_anchor: date):
        return self.session.exec(
            select(Remittance).where(
                Remittance.user_id == user_id,
                Remittance.settled_month_and_year == month_anchor,
            )
        ).first()

    def _get_worklogs(self, user_id, year: int, month: int) -> List[WorkLog]:
        return self.session.exec(
            select(WorkLog).where(
                WorkLog.user_id == user_id,
                WorkLog.year == year,
                WorkLog.month == month,
            )
        ).all()

    def _get_timelogs(self, worklog_ids: List):
        return self.session.exec(
            select(TimeLog).where(TimeLog.worklog_id.in_(worklog_ids))
        ).all()

    @staticmethod
    def _accumulate_hours_by_worklog(timelogs: List[TimeLog]):
        hours = {}
        for tl in timelogs:
            if not tl.total_time:
                continue
            h = tl.total_time.total_seconds() / 3600
            hours[tl.worklog_id] = hours.get(tl.worklog_id, 0) + h
        return hours
