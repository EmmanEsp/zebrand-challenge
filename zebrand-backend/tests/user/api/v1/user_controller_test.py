import time
from datetime import datetime
import pytest

from fastapi.testclient import TestClient


class TestUserEndpoints:
    
    email = f"{round(time.time()*1000)}@challenge.com"

    @pytest.mark.order(1)
    def test_create_user(self, admin_token: str, client: TestClient):
        response = client.post(
            url="/api/v1/user",
            json={
                "name": "string",
                "role": "admin",
                "email": self.email,
                "password": "stringstring"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        content = response.json()

        assert response.status_code == 201
        assert "data" in content
        assert content["data"] is None

    @pytest.mark.order(2)
    def test_update_user(self, admin_token: str, client: TestClient):
        response = client.patch(
            url=f"/api/v1/user/{self.email}",
            json={
                "name": f"New Name: {datetime.now()}"
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        content = response.json()

        assert response.status_code == 200
        assert "data" in content
        assert content["data"] is None

    @pytest.mark.order(3)
    def test_delete_user(self, admin_token: str, client: TestClient):
        response = client.delete(
            url=f"/api/v1/user/{self.email}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        content = response.json()

        assert response.status_code == 200
        assert "data" in content
        assert content["data"] is None
