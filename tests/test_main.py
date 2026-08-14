from fastapi.testclient import TestClient
from main import app
import pytest
client = TestClient(app)

def test_create_user():
    # Test creating a new user
    response = client.post(
        "/users/",
        json={"email": "testuser@example.com", "password": "securepassword123"}
    )
    # assert response.status_code in [201, 400]  # 201 for created, 400 if user already exists
    assert response.status_code in [201, 400]

def test_get_tasks():
    #
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)