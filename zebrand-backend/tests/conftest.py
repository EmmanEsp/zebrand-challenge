"""
Confest Testing file
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """
    Fixture client app
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def get_admin_credential(client: TestClient) -> str:
    return {"email": "string@gmail.com", "password": "stringstring"}

@pytest.fixture
def admin_token(get_admin_credential: dict, client: TestClient) -> str:

    response = client.post(
        url="/api/v1/auth/sign-in",
        json=get_admin_credential
    )

    content = response.json()

    assert response.status_code == 200
    
    return content["data"]["token"]


@pytest.fixture
def guest_token(client: TestClient) -> str:

    response = client.post(url="/api/v1/auth/guest")

    content = response.json()

    assert response.status_code == 200
    
    return content["data"]["token"]
