# tests/test_utils.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.security import hash_password, verify_password

def test_hash_and_verify_password():
    password = "TestPass123"
    
    # Hash password
    hashed, salt = hash_password(password)
    
    # Check types
    assert isinstance(hashed, str)
    assert isinstance(salt, bytes)
    
    # Correct password verification
    assert verify_password(password, hashed, salt) is True
    
    # Wrong password verification
    assert verify_password("WrongPass", hashed, salt) is False
