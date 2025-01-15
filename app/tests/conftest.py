import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.model import Base
from app.main import app, get_db
from app.models import model
from app.models.repository import Repository as FakeRepository
from app.mocks import inventory as mock_inventory


@pytest.fixture(name="session")
def session_fixture():

    engine = create_engine(
        "sqlite:///./test.db", connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):

    def get_session_override():
        yield session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def fake_repository(session) -> FakeRepository:
    return FakeRepository(session=session)


@pytest.fixture
def given_inventory(fake_repository):

    given_inventory = model.Inventory(**mock_inventory.MILK)

    fake_repository.create(given_inventory)
