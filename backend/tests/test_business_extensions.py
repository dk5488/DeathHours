from datetime import datetime, timedelta

# client fixture will be injected by pytest


def test_alert_workflow(client, headers_and_business):
    headers, business_id = headers_and_business
    payload = {"threshold_pct": 0.2, "channels": ["email", "sms"]}
    resp = client.post(f"/api/businesses/{business_id}/alerts", headers=headers, json=payload)
    assert resp.status_code == 201, resp.text
    alert = resp.json()
    assert alert["threshold_pct"] == 0.2
    assert set(alert["channels"]) == {"email", "sms"}

    # list
    resp = client.get(f"/api/businesses/{business_id}/alerts", headers=headers)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["threshold_pct"] == 0.2


def test_action_card_workflow(client, headers_and_business):
    headers, business_id = headers_and_business
    now = datetime.utcnow()
    payload = {
        "time_window_start": now.isoformat(),
        "time_window_end": (now + timedelta(hours=1)).isoformat(),
        "severity": "high",
        "headline": "Test Action",
        "copy_text": "Do this thing",
    }
    resp = client.post(f"/api/businesses/{business_id}/action_cards", headers=headers, json=payload)
    assert resp.status_code == 201, resp.text
    card = resp.json()
    assert card["severity"] == "high"
    assert card["completed"] is False

    # mark completed
    resp = client.patch(
        f"/api/businesses/{business_id}/action_cards/{card['id']}",
        headers=headers,
        json={"completed": True},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["completed"] is True


def test_report_workflow(client, headers_and_business):
    headers, business_id = headers_and_business
    start = datetime.utcnow()
    end = start + timedelta(days=7)
    payload = {"week_start": start.isoformat(), "week_end": end.isoformat(), "pdf_url": None}
    resp = client.post(f"/api/businesses/{business_id}/reports", headers=headers, json=payload)
    assert resp.status_code == 201, resp.text
    rep = resp.json()
    assert rep["week_start"] == start.isoformat()

    # list
    resp = client.get(f"/api/businesses/{business_id}/reports", headers=headers)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["week_end"] == end.isoformat()


def test_competitor_workflow(client, headers_and_business):
    headers, business_id = headers_and_business
    payload = {"name": "Comp Cafe", "google_maps_url": "https://maps.app.goo.gl/comp"}
    resp = client.post(f"/api/businesses/{business_id}/competitors", headers=headers, json=payload)
    assert resp.status_code == 201, resp.text
    comp = resp.json()
    assert comp["name"] == "Comp Cafe"

    # list
    resp = client.get(f"/api/businesses/{business_id}/competitors", headers=headers)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    assert items[0]["google_maps_url"] == "https://maps.app.goo.gl/comp"
