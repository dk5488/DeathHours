from backend.config.db import SessionLocal
from backend.models import models
from backend.service.business_service import BusinessService


def test_service_update_busy_hours(headers_and_business):
    headers, business_id = headers_and_business
    session = SessionLocal()
    try:
        # look up the owner_id from the row we just created
        biz = session.query(models.Business).filter(models.Business.id == business_id).one()
        owner_id = biz.owner_id
        payload = {"monday": [8, 9, 10], "tuesday": []}
        result = BusinessService.update_business_busy_hours(session, owner_id, business_id, payload)
        assert result is not None
        assert result["busy_hours"]["monday"] == [8, 9, 10]

        # verify the database was updated
        session.expire(biz)
        assert biz.busy_hours == payload
    finally:
        session.close()


def test_patch_busy_hours_endpoint(client, headers_and_business):
    headers, business_id = headers_and_business
    payload = {"busy_hours": {"wednesday": [12, 13]}}
    resp = client.patch(f"/api/businesses/{business_id}/busy_hours", headers=headers, json=payload)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data.get("busy_hours", {}).get("wednesday") == [12, 13]

    # GET the business and check the field is present
    resp2 = client.get(f"/api/businesses/{business_id}", headers=headers)
    assert resp2.status_code == 200
    assert resp2.json().get("busy_hours", {}).get("wednesday") == [12, 13]
