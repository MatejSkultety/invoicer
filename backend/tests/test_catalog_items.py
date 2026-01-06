import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "catalog_items.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("CORS_ORIGINS", "")
    get_settings.cache_clear()

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def sample_payload():
    return {
        "name": "Design work",
        "description": "Product design services",
        "unit": "hour",
        "unit_price": 15000,
        "tax_rate": 21,
    }


def test_create_list_get_update_delete(client, sample_payload):
    create_response = client.post("/api/catalog-items", json=sample_payload)
    assert create_response.status_code == 201
    created = create_response.json()
    item_id = created["id"]

    list_response = client.get("/api/catalog-items")
    assert list_response.status_code == 200
    listed = list_response.json()
    assert len(listed) == 1
    assert listed[0]["unit_price"] == sample_payload["unit_price"]
    assert listed[0]["tax_rate"] == sample_payload["tax_rate"]

    get_response = client.get(f"/api/catalog-items/{item_id}")
    assert get_response.status_code == 200

    updated_payload = {
        "name": "Design work updated",
        "description": "Senior design services",
        "unit": "hour",
        "unit_price": 20000,
        "tax_rate": None,
    }
    update_response = client.put(f"/api/catalog-items/{item_id}", json=updated_payload)
    assert update_response.status_code == 200
    assert update_response.json()["tax_rate"] is None

    delete_response = client.delete(f"/api/catalog-items/{item_id}")
    assert delete_response.status_code == 204

    get_deleted = client.get(f"/api/catalog-items/{item_id}")
    assert get_deleted.status_code == 404

    list_after_delete = client.get("/api/catalog-items")
    assert list_after_delete.status_code == 200
    assert list_after_delete.json() == []


def test_name_too_long_returns_validation_error(client, sample_payload):
    bad_payload = dict(sample_payload)
    bad_payload["name"] = "a" * 257

    response = client.post("/api/catalog-items", json=bad_payload)
    assert response.status_code == 422
