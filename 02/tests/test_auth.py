import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_success_registration():
    response = client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "age": 25
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert data["message"] == "User successfully registered"

def test_underage_registration():
    response = client.post("/auth/register", json={
        "username": "bob",
        "email": "bob@example.com",
        "age": 15
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "You must be at least 18 years old"

def test_forbidden_username():
    response = client.post("/auth/register", json={
        "username": "admin",
        "email": "admin@example.com",
        "age": 30
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Username 'admin' is not allowed"
