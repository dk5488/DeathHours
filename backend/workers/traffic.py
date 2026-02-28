"""Worker for ingesting foot traffic readings."""

import random
from datetime import datetime, timedelta
from typing import List

from ..config.db import SessionLocal
from ..models import models


def generate_dummy_traffic(business_id: int, count: int = 1) -> List[models.TrafficReading]:
    """Insert a few fake traffic records for the given business.

    This is a placeholder for the real scraping/integration logic that would
    contact Outscraper, PopulationMap, etc.  The public API can call this
    function when the schedule runs, or tests can invoke it directly.

    Returns the list of created objects.
    """
    session = SessionLocal()
    created: List[models.TrafficReading] = []
    try:
        for _ in range(count):
            tr = models.TrafficReading(
                business_id=business_id,
                timestamp=datetime.utcnow(),
                visitors_estimate=random.randint(0, 200),
                source="dummy",
            )
            session.add(tr)
            created.append(tr)
        session.commit()
        # refresh so ids are populated
        for tr in created:
            session.refresh(tr)
    finally:
        session.close()
    return created


def fetch_and_store_for_business(business_id: int) -> None:
    """High-level entrypoint called by a scheduler.

    In a real implementation this would:
      1. Look up the business record and its Google Maps URL.
      2. Perform an API call to fetch popular times data.
      3. Convert the returned payload into TrafficReading rows (one per hour).
      4. Insert them into the database.

    For now it just delegates to :func:`generate_dummy_traffic`.
    """
    # TODO: replace with real scraping logic
    generate_dummy_traffic(business_id, count=3)
