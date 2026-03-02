import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from backend.utils.bussiness_traffic_utils import _calculate_hour_frequency, process_and_store_busy_hours_pattern
from backend.workers.celery_app import celery_app
from backend.utils.gemini_api import generate_hour_data_from_gemini
from backend.service.business_service import BusinessService
from backend.service.traffic_reading_service import TrafficReadingService
from backend.config.db import SessionLocal
from backend.repository.business_repository import BusinessRepository

logger = logging.getLogger(__name__)


@celery_app.task(name="busy_hours_job")
def fetch_busy_hours():
    """Entrypoint that schedules individual business jobs.

    The original implementation iterated sequentially which would
    block the worker and make scaling difficult.  Here we delegate each
    business to its own task so the work can be processed concurrently by
    the Celery pool and retried independently.
    """
    logger.info("busy_hours_job triggered, fetching business list")
    # load businesses from DB
    session = SessionLocal()
    try:
        all_businesses = BusinessRepository.get_all_businesses(session)
    finally:
        session.close()
    logger.info("scheduling fetch for %d businesses", len(all_businesses))
    for business in all_businesses:
        logger.debug("enqueueing task for business_id=%s", business.id)
        fetch_busy_hours_for_business.delay(business.id, business.google_maps_url, business.owner_id)


@celery_app.task(name="busy_hours_job_for_business")
def fetch_busy_hours_for_business(business_id: int, business_url: str, owner_id: int) -> dict:
    """Fetch popular times data for a single business and persist it.

    Executed as a separate task to improve throughput and fault isolation.
    This function:
    1. Fetches busy hours from Gemini API
    2. Stores the weekly pattern in Business.busy_hours
    3. Creates TrafficReading entries for today's hours
    """
    logger.info("fetching busy hours for business_id=%s", business_id)
    hour_data = generate_hour_data_from_gemini(business_url)
    
    # update the database record using service layer
    session = SessionLocal()
    try:
        result = BusinessService.update_business_busy_hours(session, owner_id, business_id, hour_data)
        if result is None:
            logger.warning("could not update busy_hours for business_id=%s owner_id=%s", business_id, owner_id)
            return {"status": "error", "business_id": business_id}
        
        # Parse busy_hours and create TrafficReading entries for today
        _store_traffic_readings(session, business_id, hour_data)
        
        logger.info("updated busy_hours and traffic readings for business_id=%s", business_id)
        return {"status": "success", "business_id": business_id}
    finally:
        session.close()


def _store_traffic_readings(session, business_id: int, hour_data: dict) -> None:
    """Parse busy hours data and store data-driven busyness patterns.
    
    Calculates busyness_score for each hour based on frequency across the week:
    busyness_score = (days_hour_appears_busy / 7) * 100
    
    Handles both time formats:
    - Integer format: 9 (hour 9)
    - Range format: "20-21" (extract start hour: 20)
    
    For example:
    - If hour 9 is busy on 6 days: busyness_score = 85.71%
    - If hour 8 is busy on 2 days: busyness_score = 28.57%
    - If hour 15 is never busy: busyness_score = 0%
    
    Args:
        session: SQLAlchemy session
        business_id: Business ID
        hour_data: Dict with day names as keys and lists of busy hours as values
                   Supports both formats:
                   - Integer: {"monday": [8, 9, 10]}
                   - Range: {"monday": ["8-9", "9-10", "10-11"]}
    """
    day_name_to_dow = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    
    logger.debug("calculating data-driven busyness scores for business_id=%s", business_id)
    
    # Step 1: Parse hour_data to convert range format to integers if needed
    parsed_hour_data = process_and_store_busy_hours_pattern(hour_data)
    
    logger.debug("parsed_hour_data for business_id=%s: %s", business_id, parsed_hour_data)
    
    # Step 2: Calculate frequency for each hour across the week
    hour_frequency = _calculate_hour_frequency(parsed_hour_data)
    logger.debug("hour_frequency for business_id=%s: %s", business_id, hour_frequency)
    
    # Step 3: Store pattern data for all day/hour combinations using business timezone
    business = BusinessRepository.get_business_by_id(session, business_id)
    tz_name = (business.timezone or "UTC") if business is not None else "UTC"
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        logger.warning("invalid timezone %s for business %s, falling back to UTC", tz_name, business_id)
        tz = ZoneInfo("UTC")

    # Determine local current day (Monday=0) for synthetic timestamps
    now_local = datetime.now(tz)
    local_monday = (now_local - timedelta(days=now_local.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    current_day_of_week = now_local.weekday()
    next_day_of_week = (current_day_of_week + 1) % 7

    # Normalize parsed_hour_data keys to lowercase for lookup
    normalized_parsed = {k.lower(): set(v) for k, v in parsed_hour_data.items()}

    # Map dow -> day name
    dow_to_name = {v: k for k, v in day_name_to_dow.items()}

    logger.debug("storing busy hour patterns for business_id=%s for current day (dow=%s) and next day (dow=%s)", 
                 business_id, current_day_of_week, next_day_of_week)

    # Store patterns for both current day and next day
    for day_offset, day_of_week in [(0, current_day_of_week), (1, next_day_of_week)]:
        day_name = dow_to_name.get(day_of_week)
        if day_name is None:
            logger.warning("could not determine day name for dow=%s, skipping pattern store", day_of_week)
            continue

        busy_hours_for_day = normalized_parsed.get(day_name, set())

        for hour in range(24):
            is_busy = hour in busy_hours_for_day
            # Use data-driven busyness score based on frequency across the week
            busyness_score = hour_frequency.get(hour, 0.0)

            # Construct a timezone-aware synthetic timestamp for this day/hour
            local_dt = local_monday + timedelta(days=day_of_week, hours=hour)
            # Convert to UTC for storage (database stores UTC-naive datetimes)
            utc_dt = local_dt.astimezone(ZoneInfo("UTC")).replace(tzinfo=None)

            TrafficReadingService.upsert_busy_hours_pattern(
                session=session,
                business_id=business_id,
                day_of_week=day_of_week,
                hour=hour,
                is_busy=is_busy,
                busyness_score=busyness_score,
                synthetic_timestamp=utc_dt,
            )
    
    logger.info("created/updated busy hour patterns for business_id=%s with frequency-based busyness scores (48 rows total for current and next day)", business_id)




