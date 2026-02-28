import os
import sys
import pytest
from fastapi.testclient import TestClient

# ensure project root is on path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.main import app
from backend.config.db import init_db


@pytest.fixture(scope="session", autouse=True)
def setup_module():
    # ensure clean database before any tests
    url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    # compute file path for sqlite url and normalize
    path = None
    if url.startswith("sqlite"):
        # handle both triple and quadruple slash cases
        # split only on first occurrence
        path = url.split("///", 1)[1]
        if not os.path.isabs(path):
            path = os.path.abspath(path)
    print(f"[conftest] setup_module raw_url={url} resolved_path={path}")
    if path and os.path.exists(path):
        print(f"[conftest] pre-remove exists size={os.path.getsize(path)} mode={oct(os.stat(path).st_mode)}")
        try:
            os.remove(path)
        except Exception as e:
            print(f"[conftest] remove error {e}")
    print(f"[conftest] after remove exists={os.path.exists(path) if path else None}")
    init_db()
    if path:
        print(f"[conftest] after init_db exists={os.path.exists(path)} size={os.path.getsize(path)}")


@pytest.fixture(scope="session")
def client():
    # create TestClient after DB has been set up
    with TestClient(app) as c:
        yield c


import uuid

@pytest.fixture
def headers_and_business(client):
    # create user with unique address and login
    email = f"test+{uuid.uuid4().hex}@example.com"
    resp = client.post(
        "/api/users",
        json={"email": email, "password": "secret"},
    )
    assert resp.status_code == 201, resp.text
    resp = client.post(
        "/api/token", data={"username": email, "password": "secret"}
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # create business with unique maps url to avoid constraint collisions
    maps_url = f"https://maps.app.goo.gl/test-{uuid.uuid4().hex}"
    resp = client.post(
        "/api/businesses",
        headers=headers,
        json={"google_maps_url": maps_url, "name": "My Cafe", "category": "cafe"},
    )
    assert resp.status_code == 200, resp.text
    business = resp.json()
    return headers, business["id"]
