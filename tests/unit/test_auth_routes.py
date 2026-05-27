from fastapi.testclient import TestClient

from farmer_helper.core.config import get_settings
from farmer_helper.db.base import get_engine
from farmer_helper.db.models.base import Base
from farmer_helper.main import app


def _reset_db() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def _api_key_headers() -> dict[str, str]:
    api_key = get_settings().security_api_key
    if api_key is None:
        return {}
    return {"x-api-key": api_key}


def test_default_admin_can_login_and_resolve_current_user() -> None:
    _reset_db()
    client = TestClient(app)

    login = client.post("/auth/login", json={"username": "admin", "password": "P@ssw0rd"})

    assert login.status_code == 200
    payload = login.json()
    assert payload["token_type"] == "bearer"
    assert payload["user"]["username"] == "admin"
    assert payload["user"]["role"] == "admin"

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {payload['access_token']}"})
    assert me.status_code == 200
    assert me.json()["role"] == "admin"


def test_register_creates_user_role_account_and_me_response() -> None:
    _reset_db()
    client = TestClient(app)

    registered = client.post(
        "/auth/register",
        json={"username": "field-user", "password": "correct-horse-battery"},
    )

    assert registered.status_code == 201
    payload = registered.json()
    assert payload["user"]["username"] == "field-user"
    assert payload["user"]["role"] == "user"

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {payload['access_token']}"})
    assert me.status_code == 200
    assert me.json() == payload["user"]


def test_user_role_cannot_access_admin_endpoints() -> None:
    _reset_db()
    client = TestClient(app)
    registered = client.post(
        "/auth/register",
        json={"username": "field-user", "password": "correct-horse-battery"},
    )
    token = registered.json()["access_token"]

    denied = client.get(
        "/admin/access-audit",
        headers={**_api_key_headers(), "Authorization": f"Bearer {token}"},
    )

    assert denied.status_code == 403
    assert denied.json()["detail"] == "Admin role required"


def test_anonymous_admin_request_is_rejected() -> None:
    _reset_db()
    client = TestClient(app)

    denied = client.get("/admin/access-audit", headers=_api_key_headers())

    assert denied.status_code == 401
    assert denied.json()["detail"] == "Authentication required"
