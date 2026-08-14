from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)


def test_create_user():
    # Create a unique email every time the test runs
    unique_email = f"testuser_{uuid.uuid4().hex}@example.com"

    response = client.post(
        "/users/",
        json={
            "email": unique_email,
            "password": "securepassword123"
        }
    )

    assert response.status_code == 201


def test_get_tasks():
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)