from fastapi.testclient import TestClient

class TestAuthEndpoints:

    def test_auth_guest(self, client: TestClient):
        response = client.post("/api/v1/auth/guest")

        content = response.json()

        assert response.status_code == 200
        assert "data" in content
        assert "token" in content["data"]

    def test_auth_signin(self, get_admin_credential: dict, client: TestClient):
        response = client.post(
            url="/api/v1/auth/sign-in",
            json=get_admin_credential
        )

        content = response.json()

        assert response.status_code == 200
        assert "data" in content
        assert "token" in content["data"]
