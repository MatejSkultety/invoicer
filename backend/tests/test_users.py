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
def required_payload():
    return {
        "name": "Acme Co",
        "address": "123 Main St",
        "city": "Prague",
        "country": "Czechia",
        "trade_licensing_office": "Prague 1",
    }


@pytest.fixture()
def sample_payload(required_payload):
    return {
        **required_payload,
        "email": "billing@acme.test",
        "phone": "+420123456789",
        "bank": "Example Bank",
        "iban": "CZ6508000000192000145399",
        "swift": "GIBACZPX",
        "ico": "12345678",
        "dic": "CZ12345678",
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
    assert (
        fetched["trade_licensing_office"]
        == sample_payload["trade_licensing_office"]
    )
    assert fetched["email"] == sample_payload["email"]

    updated_payload = dict(sample_payload)
    updated_payload["name"] = "Acme Updated"
    updated_payload["email"] = None

    update_response = client.put("/api/users/me", json=updated_payload)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Acme Updated"
    assert update_response.json()["email"] is None


def test_name_too_long_returns_validation_error(client, sample_payload):
    bad_payload = dict(sample_payload)
    bad_payload["name"] = "a" * 257

    response = client.put("/api/users/me", json=bad_payload)
    assert response.status_code == 422


def test_optional_fields_can_be_set_and_cleared(client, required_payload):
    create_response = client.put("/api/users/me", json=required_payload)
    assert create_response.status_code == 200
    created = create_response.json()
    assert created["email"] is None
    assert created["phone"] is None
    assert created["bank"] is None
    assert created["iban"] is None
    assert created["swift"] is None
    assert created["ico"] is None
    assert created["dic"] is None

    update_payload = {
        **required_payload,
        "email": "hello@acme.test",
        "phone": "+420777888999",
        "bank": "Updated Bank",
        "iban": "DE12500105170648489890",
        "swift": "DEUTDEFF",
        "ico": "87654321",
        "dic": "CZ87654321",
    }
    update_response = client.put("/api/users/me", json=update_payload)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["email"] == update_payload["email"]
    assert updated["phone"] == update_payload["phone"]
    assert updated["bank"] == update_payload["bank"]
    assert updated["iban"] == update_payload["iban"]
    assert updated["swift"] == update_payload["swift"]
    assert updated["ico"] == update_payload["ico"]
    assert updated["dic"] == update_payload["dic"]

    clear_payload = {**required_payload, "email": None, "phone": None, "bank": None, "iban": None, "swift": None, "ico": None, "dic": None}
    clear_response = client.put("/api/users/me", json=clear_payload)
    assert clear_response.status_code == 200
    cleared = clear_response.json()
    assert cleared["email"] is None
    assert cleared["phone"] is None
    assert cleared["bank"] is None
    assert cleared["iban"] is None
    assert cleared["swift"] is None
    assert cleared["ico"] is None
    assert cleared["dic"] is None


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", ""),
        ("address", ""),
        ("city", ""),
        ("country", ""),
        ("trade_licensing_office", ""),
    ],
)
def test_required_fields_cannot_be_cleared(client, sample_payload, field, value):
    bad_payload = dict(sample_payload)
    bad_payload[field] = value

    response = client.put("/api/users/me", json=bad_payload)
    assert response.status_code == 422
