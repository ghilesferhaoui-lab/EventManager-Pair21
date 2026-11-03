import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_create_and_fetch_event_integration():
    response = client.post("/events/", json={
        "title": "DevOps Integration Conf",
        "location": "Constantine",
        "date": "2026-12-01",
        "capacity": 200
    })

    assert response.status_code == 201

    event_id = response.json()["id"]

    get_resp = client.get(f"/events/{event_id}")

    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "DevOps Integration Conf"


def test_register_participant_to_event_integration():
    e_resp = client.post("/events/", json={
        "title": "Cybersecurity Workshop",
        "location": "NTIC",
        "date": "2026-12-01",
        "capacity": 50
    })

    assert e_resp.status_code == 201
    event_id = e_resp.json()["id"]

    p_resp = client.post("/participants/", json={
        "name": "Alice Dev",
        "email": "alice.integration@example.com"
    })

    assert p_resp.status_code == 201
    part_id = p_resp.json()["id"]

    reg_resp = client.post(
        f"/events/{event_id}/register/{part_id}"
    )

    assert reg_resp.status_code == 201

    list_resp = client.get(
        f"/events/{event_id}/participants"
    )

    assert list_resp.status_code == 200
    assert any(
        p["id"] == part_id
        for p in list_resp.json()
    )


def test_register_non_existent_event_returns_404():
    response = client.post("/events/9999/register/1")

    assert response.status_code == 404


