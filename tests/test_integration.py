from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_add():
    response = client.get("/calculate/add?a=2&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_api_subtract():
    response = client.get("/calculate/subtract?a=10&b=4")
    assert response.status_code == 200
    assert response.json()["result"] == 6

def test_api_multiply():
    response = client.get("/calculate/multiply?a=1&b=4")
    assert response.status_code == 200
    assert response.json()["result"] == 4

def test_api_divide():
    response = client.get("/calculate/divide?a=12&b=4")
    assert response.status_code == 200
    assert response.json()["result"] == 3

def test_divide_by_zero():
    response = client.get("/calculate/divide?a=5&b=0")
    assert response.status_code == 400 or response.status_code == 422

def test_api_power():
    response = client.get("/calculate/power?a=2&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 8

def test_api_root():
    response = client.get("/calculate/root?a=16&b=2")
    assert response.status_code == 200
    assert response.json()["result"] == 4

def test_api_modulus():
    response = client.get("/calculate/modulus?a=10&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 1

def test_api_absolute_difference():
    response = client.get("/calculate/absolutedifference?a=5&b=9")
    assert response.status_code == 200
    assert response.json()["result"] == 4

def test_api_percentage():
    response = client.get("/calculate/percentage?a=25&b=200")
    assert response.status_code == 200
    assert response.json()["result"] == 12.5

def test_api_integerdivision():
    response = client.get("/calculate/integerdivision?a=10&b=3")
    assert response.status_code == 200
    assert response.json()["result"] == 3
