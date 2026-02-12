# tests/conftest.py
import pytest
from sqlmodel import SQLModel, create_engine
from sqlmodel import Session
from fastapi.testclient import TestClient
from app.infrastructure.db.session import get_session
from sqlalchemy.pool import StaticPool
# from app import main
from app.main import app


TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


# tests/conftest.py
@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session
        session.rollback()


# tests/conftest.py
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
