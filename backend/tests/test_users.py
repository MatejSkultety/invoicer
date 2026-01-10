import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "users.db"
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
        "trade_licensing_office": "Prague 1",
        "ico": "12345678",
        "dic": "CZ12345678",
        "email": "billing@acme.test",
        "phone": "+420123456789",
        "bank": "Example Bank",
        "iban": "CZ6508000000192000145399",
        "swift": "GIBACZPX",
    }


def test_get_missing_user_returns_404(client):
    response = client.get("/api/users/me")
    assert response.status_code == 404


def test_upsert_and_get_user_profile(client, sample_payload):
    upsert_response = client.put("/api/users/me", json=sample_payload)
    assert upsert_response.status_code == 200
    created = upsert_response.json()
    assert created["id"] == "local-user"

    get_response = client.get("/api/users/me")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["name"] == sample_payload["name"]
    assert fetched["trade_licensing_office"] == sample_payload["trade_licensing_office"]
    assert fetched["email"] == sample_payload["email"]

    updated_payload = dict(sample_payload)
    updated_payload["name"] = "Acme Updated"
    updated_payload["bank"] = "Updated Bank"

    update_response = client.put("/api/users/me", json=updated_payload)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Acme Updated"
    assert update_response.json()["bank"] == "Updated Bank"


def test_name_too_long_returns_validation_error(client, sample_payload):
    bad_payload = dict(sample_payload)
    bad_payload["name"] = "a" * 257

    response = client.put("/api/users/me", json=bad_payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", ""),
        ("address", ""),
        ("city", ""),
        ("country", ""),
        ("trade_licensing_office", ""),
        ("ico", ""),
        ("dic", ""),
        ("email", ""),
        ("phone", ""),
        ("bank", ""),
        ("iban", ""),
        ("swift", ""),
    ],
)
def test_required_fields_cannot_be_cleared(client, sample_payload, field, value):
    bad_payload = dict(sample_payload)
    bad_payload[field] = value

    response = client.put("/api/users/me", json=bad_payload)
    assert response.status_code == 422
