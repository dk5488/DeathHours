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


def test_store_pattern_only_current_day(headers_and_business):
    """Ensure busy-hours pattern upsert only creates rows for today's day_of_week."""
    headers, business_id = headers_and_business
    # prepare session and clear any existing readings
    session = SessionLocal()
    try:
        session.query(models.TrafficReading).filter(models.TrafficReading.business_id == business_id).delete()
        session.commit()
        # grab business metadata (timezone)
        from backend.repository.business_repository import BusinessRepository
        business = BusinessRepository.get_business_by_id(session, business_id)
        tz_name = business.timezone or "UTC"
        from zoneinfo import ZoneInfo
        from datetime import datetime
        now_local = datetime.now(ZoneInfo(tz_name))
        current_dow = now_local.weekday()

        # supply hour_data with values for every day
        hour_data = {
            "monday": [0, 1],
            "tuesday": [2],
            "wednesday": [3],
            "thursday": [4],
            "friday": [5],
            "saturday": [6],
            "sunday": [7],
        }

        # call private helper directly
        from backend.workers.jobs.busy_hours_job import _store_traffic_readings
        _store_traffic_readings(session, business_id, hour_data)

        # count entries by dow
        counts = {}
        for i in range(7):
            counts[i] = (
                session.query(models.TrafficReading)
                .filter(
                    models.TrafficReading.business_id == business_id,
                    models.TrafficReading.day_of_week == i,
                )
                .count()
            )

        assert counts[current_dow] == 24, f"expected 24 rows for current dow {current_dow}, got {counts[current_dow]}"
        for i in range(7):
            if i != current_dow:
                assert counts[i] == 0, f"unexpected rows for dow {i}: {counts[i]}"
    finally:
        session.close()
