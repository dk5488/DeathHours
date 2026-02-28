from datetime import datetime, timedelta

from backend.tests.conftest import client
from backend.workers import traffic
from backend.config.db import SessionLocal
from backend.models import models


def test_generate_dummy_traffic(headers_and_business):
    headers, business_id = headers_and_business
    # ensure no readings exist yet
    session = SessionLocal()
    try:
        before = session.query(models.TrafficReading).filter(models.TrafficReading.business_id == business_id).count()
        assert before == 0
    finally:
        session.close()

    created = traffic.generate_dummy_traffic(business_id, count=2)
    assert len(created) == 2
    assert all(isinstance(r, models.TrafficReading) for r in created)

    session = SessionLocal()
    try:
        after = session.query(models.TrafficReading).filter(models.TrafficReading.business_id == business_id).count()
        assert after == 2
    finally:
        session.close()


def test_fetch_and_store_for_business(headers_and_business):
    headers, business_id = headers_and_business
    # fetch_and_store should insert three records
    traffic.fetch_and_store_for_business(business_id)
    session = SessionLocal()
    try:
        count = session.query(models.TrafficReading).filter(models.TrafficReading.business_id == business_id).count()
        assert count >= 3
    finally:
        session.close()
