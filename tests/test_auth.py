# import pytest
# from fastapi.testclient import TestClient
# from main import app
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.models import Base
# import os
# import time

# client = TestClient(app)

# # Ensure database is ready for integration tests
# @pytest.fixture(scope="session", autouse=True)
# def setup_db():
#     url = os.getenv("DATABASE_URL")
#     engine = create_engine(url)

#     # Wait for DB
#     start = time.time()
#     while True:
#         try:
#             conn = engine.connect()
#             conn.close()
#             break
#         except Exception:
#             if time.time() - start > 30:
#                 raise TimeoutError("Database did not become available in time")
#             time.sleep(1)

#     # Create tables
#     Base.metadata.create_all(engine)
#     yield
#     # Optional: drop tables after tests
#     Base.metadata.drop_all(engine)

# def test_register_login_flow():
#     # Register user
#     response = client.post("/register", json={
#         "username": "tester2",
#         "email": "tester2@example.com",
#         "password": "TestPass123"
#     })
#     assert response.status_code == 200
#     assert "tester2" in response.json().get("message", "")

#     # Login success
#     response = client.post("/login", json={
#         "username": "tester2",
#         "password": "TestPass123"
#     })
#     assert response.status_code == 200
#     assert "Welcome" in response.json()["message"]

#     # Login failure
#     response = client.post("/login", json={
#         "username": "tester2",
#         "password": "WrongPass"
#     })
#     assert response.status_code == 400
