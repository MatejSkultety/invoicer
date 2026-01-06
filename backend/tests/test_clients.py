import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "clients.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("CORS_ORIGINS", "")
    get_settings.cache_clear()

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def sample_payload():
    return {
        "name": "Acme Co",
        "address": "123 Main St",
        "city": "Prague",
        "country": "Czechia",
        "main_contact_method": "email",
        "main_contact": "hello@acme.test",
        "additional_contact": "secondary@acme.test",
        "ico": "12345678",
        "dic": "CZ12345678",
        "notes": "Priority account",
        "favourite": True,
    }


def test_create_list_get_update_delete(client, sample_payload):
    create_response = client.post("/api/clients", json=sample_payload)
    assert create_response.status_code == 201
    created = create_response.json()
    client_id = created["id"]

    list_response = client.get("/api/clients")
    assert list_response.status_code == 200
    listed = list_response.json()
    assert len(listed) == 1
    assert listed[0]["main_contact"] == sample_payload["main_contact"]
    assert listed[0]["favourite"] is True
    assert isinstance(listed[0]["id"], str)

    get_response = client.get(f"/api/clients/{client_id}")
    assert get_response.status_code == 200

    updated_payload = {
        "name": "Acme Updated",
        "address": "456 Market St",
        "city": "Brno",
        "country": "Czechia",
        "main_contact_method": "whatsapp",
        "main_contact": "+420123456789",
        "additional_contact": None,
        "ico": "87654321",
        "dic": "CZ87654321",
        "notes": None,
        "favourite": False,
    }
    update_response = client.put(f"/api/clients/{client_id}", json=updated_payload)
    assert update_response.status_code == 200
    assert update_response.json()["main_contact_method"] == "whatsapp"
    assert update_response.json()["favourite"] is False

    delete_response = client.delete(f"/api/clients/{client_id}")
    assert delete_response.status_code == 204

    get_deleted = client.get(f"/api/clients/{client_id}")
    assert get_deleted.status_code == 404

    list_after_delete = client.get("/api/clients")
    assert list_after_delete.status_code == 200
    assert list_after_delete.json() == []

    recreate_response = client.post("/api/clients", json=sample_payload)
    assert recreate_response.status_code == 201


def test_invalid_contact_method_returns_validation_error(client, sample_payload):
    bad_payload = dict(sample_payload)
    bad_payload["main_contact_method"] = "sms"

    response = client.post("/api/clients", json=bad_payload)
    assert response.status_code == 422


def test_name_too_long_returns_validation_error(client, sample_payload):
    bad_payload = dict(sample_payload)
    bad_payload["name"] = "a" * 257

    response = client.post("/api/clients", json=bad_payload)
    assert response.status_code == 422
