# tests/test_utils.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.security import hash_password, verify_password

def test_hash_and_verify_password():
    password = "TestPass123"

    # Hash password
    hashed = hash_password(password)  # only one value

    # Verify password
    assert verify_password(password, hashed)

