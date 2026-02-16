from uuid import uuid4, UUID
from datetime import date

from sqlmodel import select

from app.infrastructure.db.models import WorkLog


def test_create_worklog_success(client, session):
    user_id = str(uuid4())
    task_id = str(uuid4())
    task_assignment_id = str(uuid4())
    target_year = 2024
    target_month = 12

    response = client.post(
        "/worklogs/create-worklog/",
        json={
            "user_id": user_id,
            "task_id": task_id,
            "task_assignment_id": task_assignment_id,
            "year": target_year,
            "month": target_month,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == user_id
    assert body["task_id"] == task_id
    assert body["task_assignment_id"] == task_assignment_id
    assert body["year"] == target_year
    assert body["month"] == target_month

    rows = session.exec(
        select(WorkLog).where(
            WorkLog.user_id == UUID(body["user_id"]),
            WorkLog.task_id == UUID(body["task_id"]),
            WorkLog.year == body["year"],
            WorkLog.month == body["month"],
        )
    ).all()
    assert len(rows) == 1


def test_create_worklog_idempotent_same_month(client, session):
    user_id = str(uuid4())
    task_id = str(uuid4())
    task_assignment_id = str(uuid4())
    payload = {
        "user_id": user_id,
        "task_id": task_id,
        "task_assignment_id": task_assignment_id,
        "year": date.today().year,
        "month": date.today().month,
    }

    first = client.post(
        "/worklogs/create-worklog/",
        json=payload,
    )
    assert first.status_code == 200

    second = client.post(
        "/worklogs/create-worklog/",
        json=payload,
    )
    assert second.status_code == 200

    first_body = first.json()
    rows = session.exec(
        select(WorkLog).where(
            WorkLog.user_id == UUID(first_body["user_id"]),
            WorkLog.task_id == UUID(first_body["task_id"]),
            WorkLog.year == first_body["year"],
            WorkLog.month == first_body["month"],
        )
    ).all()
    assert len(rows) == 1
