from datetime import datetime, timedelta

# client fixture is provided by conftest

from backend.models import models, schemas


def create_user_and_business(client):
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


def test_event_workflow(client):
    headers, business_id = create_user_and_business(client)
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
