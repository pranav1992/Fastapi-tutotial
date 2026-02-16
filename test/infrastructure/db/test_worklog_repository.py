from datetime import date
from uuid import uuid4

from sqlmodel import select, delete

from app.infrastructure.db.repositories.worklog_repo import WorkLogRepository
from app.infrastructure.db.models import WorkLog
from app.domain.schema import WorkLogCreate


def test_create_worklog_new_record(session):
    session.exec(delete(WorkLog))
    session.commit()
    repo = WorkLogRepository(session)
    user_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    task_id = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    task_assignment_id = str(uuid4())

    worklog = repo.create_worklog(WorkLogCreate(
        user_id=user_id,
        task_id=task_id,
        task_assignment_id=task_assignment_id,
        year=date.today().year,
        month=date.today().month,
    ))

    assert worklog.id is not None
    assert str(worklog.user_id) == user_id
    assert str(worklog.task_id) == task_id
    assert str(worklog.task_assignment_id) == task_assignment_id
    assert worklog.month == date.today().month
    assert worklog.year == date.today().year

    stored = session.exec(select(WorkLog)).all()
    assert len(stored) == 1


def test_create_worklog_returns_existing_for_same_month(session):
    session.exec(delete(WorkLog))
    session.commit()
    repo = WorkLogRepository(session)
    user_id = "cccccccc-cccc-cccc-cccc-cccccccccccc"
    task_id = "dddddddd-dddd-dddd-dddd-dddddddddddd"
    task_assignment_id = str(uuid4())

    payload = WorkLogCreate(
        user_id=user_id,
        task_id=task_id,
        task_assignment_id=task_assignment_id,
        year=date.today().year,
        month=date.today().month,
    )
    first = repo.create_worklog(payload)
    second = repo.create_worklog(payload)

    assert second.id == first.id
    count = session.exec(
        select(WorkLog).where(
            WorkLog.user_id == first.user_id,
            WorkLog.task_id == first.task_id,
            WorkLog.task_assignment_id == first.task_assignment_id,
            WorkLog.year == first.year,
            WorkLog.month == first.month,
        )
    ).all()
    assert len(count) == 1


def test_create_worklog_respects_target_date(session):
    session.exec(delete(WorkLog))
    session.commit()
    repo = WorkLogRepository(session)
    user_id = "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"
    task_id = "ffffffff-ffff-ffff-ffff-ffffffffffff"
    task_assignment_id = str(uuid4())
    target = date(2024, 12, 5)

    worklog = repo.create_worklog(WorkLogCreate(
        user_id=user_id,
        task_id=task_id,
        task_assignment_id=task_assignment_id,
        year=target.year,
        month=target.month,
    ))

    assert worklog.year == 2024
    assert worklog.month == 12
