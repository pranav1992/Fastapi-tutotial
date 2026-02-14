from uuid import uuid4, UUID

from sqlmodel import select

from app.infrastructure.db.models import WorkLog


def test_create_worklog_success(client, session):
    user_id = str(uuid4())
    task_id = str(uuid4())

    response = client.post(
        "/worklogs/",
        json={
            "user_id": user_id,
            "task_id": task_id,
            "target_date": "2024-12-05",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == user_id
    assert body["task_id"] == task_id
    assert body["year"] == 2024
    assert body["month"] == 12

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

    first = client.post(
        "/worklogs/",
        json={"user_id": user_id, "task_id": task_id},
    )
    assert first.status_code == 200

    second = client.post(
        "/worklogs/",
        json={"user_id": user_id, "task_id": task_id},
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
