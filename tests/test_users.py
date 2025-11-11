# tests/test_users.py
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime

from main import app
from app.database import get_db
from app.schemas import UserCreate

client = TestClient(app)

# Fake DB dependency
def fake_db():
    class FakeUser:
        id = 1
        username = "tester"
        email = "tester@example.com"
        password_hash = "hashedpassword"
        created_at = datetime.utcnow()
    
    db = MagicMock()
    db.query().filter().first.return_value = None  # No existing user
    db.add.return_value = None
    db.commit.return_value = None
    # When refresh is called, set id and created_at
    db.refresh.side_effect = lambda x: setattr(x, "id", 1) or setattr(x, "created_at", datetime.utcnow())
    
    return db

# Override get_db dependency
app.dependency_overrides[get_db] = fake_db

def test_create_user_route():
    with patch("app.routes_users.security.hash_password", return_value="hashedpassword"):
        response = client.post("/users/", json={
            "username": "tester",
            "email": "tester@example.com",
            "password": "TestPass123"
        })
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "tester"
    assert data["email"] == "tester@example.com"
    assert "created_at" in data
