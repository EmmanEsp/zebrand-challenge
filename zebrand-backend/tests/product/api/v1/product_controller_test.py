import time
import pytest

from fastapi.testclient import TestClient


class TestProductEndpoints:
    sku = f"{round(time.time()*1000)}"[:9]

    @pytest.mark.order(1)
    def test_create_product(self, admin_token: str, client: TestClient):
        payload = {
            "sku": self.sku,
            "name": "string",
            "price": 1.99,
            "brand": "string"
        }
        print(payload)
        response = client.post(
            url="/api/v1/products",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=payload
        )

        content = response.json()

        assert response.status_code == 201
        assert content["service_status"] == "ok"
        assert content["status_code"] == 201

    @pytest.mark.order(2)
    def test_get_all_products(self, admin_token: str, client: TestClient):

        response = client.get(
            url="/api/v1/products",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        content = response.json()

        assert response.status_code == 200
        assert content["service_status"] == "ok"
        assert content["status_code"] == 200

    @pytest.mark.order(3)
    def test_get_product_by_sku(self, admin_token: str, client: TestClient):

        response = client.get(
            url=f"/api/v1/products/sku/{self.sku}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )

        content = response.json()

        assert response.status_code == 200
        assert content["service_status"] == "ok"
        assert content["status_code"] == 200
