from fastapi.testclient import TestClient
import os
import sys
from datetime import datetime, timedelta

# ensure project root is on path so imports work
# test module location: backend/tests, so parent parent is workspace root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.main import app
from backend.config.db import init_db
from backend.models import models, schemas
from backend.config import db as db_module

client = TestClient(app)


def setup_module(module):
    # ensure clean database
    # remove any existing sqlite file if present
    url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    if url.startswith("sqlite"):
        path = url.split("///")[-1]
        try:
            os.remove(path)
        except Exception:
            pass
    init_db()


def create_user_and_business():
    # create a user
    resp = client.post(
        "/api/users",
        json={"email": "test@example.com", "password": "secret"},
    )
    assert resp.status_code == 201
    # login
    resp = client.post(
        "/api/token", data={"username": "test@example.com", "password": "secret"}
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # create a business
    resp = client.post(
        "/api/businesses",
        headers=headers,
        json={"google_maps_url": "https://maps.app.goo.gl/test", "name": "My Cafe", "category": "cafe"},
    )
    assert resp.status_code == 200
    business = resp.json()
    return headers, business["id"]


def test_event_workflow():
    headers, business_id = create_user_and_business()
    # create event
    now = datetime.utcnow()
    event_payload = {
        "name": "Concert",
        "start_time": now.isoformat(),
        "end_time": (now + timedelta(hours=2)).isoformat(),
        "distance_meters": 500.0,
        "impact_score": 0.8,
        "raw_data": {"source": "eventbrite"},
    }
    resp = client.post(f"/api/businesses/{business_id}/events", headers=headers, json=event_payload)
    assert resp.status_code == 201, resp.text
    event = resp.json()
    assert event["name"] == "Concert"

    # list events
    resp = client.get(f"/api/businesses/{business_id}/events", headers=headers)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["name"] == "Concert"
