import os
import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # your SQLAlchemy Base
from main import app

# Test DB URL (make sure it's separate from production!)
os.environ["DATABASE_URL"] = "postgresql+psycopg2://postgres:postgres@localhost:5432/fastapi_test_db"

@pytest.fixture(scope="session")
def engine():
    url = os.getenv("DATABASE_URL")
    eng = create_engine(url)
    
    # Wait for DB to be ready
    start = time.time()
    timeout = 30
    while True:
        try:
            conn = eng.connect()
            conn.close()
            break
        except Exception:
            if time.time() - start > timeout:
                raise TimeoutError("Database did not become available in time")
            time.sleep(1)

    # Create tables
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)

@pytest.fixture(scope="function")
def db_session(engine):
    """Creates a new session for each test"""
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope="module")
def client():
    """FastAPI test client"""
    return TestClient(app)
