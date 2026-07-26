"""Shared isolated database setup for API tests."""

import os
from pathlib import Path

# This must be set before importing the application, which initializes its
# SQLAlchemy engine at import time.  The file is intentionally outside the
# project and is removed when the pytest session finishes.
TEST_DATABASE_PATH = Path("/tmp/hsr_light_cones_pytest.sqlite3")
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DATABASE_PATH}"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

import db_models
from database import Base, SessionLocal, engine
from main import app


@pytest.fixture(scope="session", autouse=True)
def test_database():
    """Create and remove a database used only by the test suite."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    TEST_DATABASE_PATH.unlink(missing_ok=True)


@pytest.fixture(autouse=True)
def clean_light_cones():
    """Keep every test independent while retaining the test schema."""
    with SessionLocal() as session:
        session.execute(delete(db_models.LightConeDB))
        session.commit()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def light_cone_payload():
    return {
        "id": 1,
        "name": "This Love, Forever",
        "stars": 5,
        "atk": 476,
        "hp": 1270,
        "defense": 463,
        "level": 80,
        "rank": 1,
        "description": "Signature Light Cone of Cyrene.",
    }
