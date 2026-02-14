
from fastapi.testclient import TestClient

from app.application.services.worklog_service import WorkLogService
from app.domain.exceptions import WorkLogAlreadyExists
from app.main import app
from app.infrastructure.db.session import get_session
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool


def test_worklog_already_exists_exception(monkeypatch):
    # Isolate app with fresh in-memory DB
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    # Force service to raise the domain error
    monkeypatch.setattr(
        WorkLogService,
        "create_worklog",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            WorkLogAlreadyExists("Worklog already exists")
        ),
    )

    client = TestClient(app)
    resp = client.post(
        "/worklogs/",
        json={"user_id": "11111111-1111-1111-1111-111111111111",
              "task_id": "22222222-2222-2222-2222-222222222222"},
    )

    assert resp.status_code == 409
    assert resp.json()["message"] == "Worklog already exists"

    app.dependency_overrides.clear()
