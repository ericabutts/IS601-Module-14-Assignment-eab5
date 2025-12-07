# tests/test_users.py
import pytest
from unittest.mock import MagicMock
from app import crud, security
from datetime import datetime

@pytest.mark.parametrize(
    "username,email,password",
    [
        ("testuser1", "user1@example.com", "Password123"),
        ("testuser2", "user2@example.com", "Password456")
    ]
)
def test_register_user(username, email, password):
    # Fake user input object
    class UserIn:
        def __init__(self, username, email, password):
            self.username = username
            self.email = email
            self.password = password

    user_in = UserIn(username=username, email=email, password=password)

    # Mock session
    mock_db = MagicMock()
    
    # Call the CRUD function with the mock
    user = crud.create_user(mock_db, user_in)

    # Check that db.add, db.commit, db.refresh were called
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(user)

    # Check that password is hashed
    assert security.verify_password(password, user.password_hash)
    assert user.username == username
    assert user.email == email
