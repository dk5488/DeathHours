import logging

from backend.workers.celery_app import celery_app
from backend.utils.gemini_api import generate_hour_data_from_gemini
from backend.service.business_service import BusinessService
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
    """
    logger.info("fetching busy hours for business_id=%s", business_id)
    hour_data = generate_hour_data_from_gemini(business_url)
    # update the database record using service layer (returns JSON)
    session = SessionLocal()
    try:
        result = BusinessService.update_business_busy_hours(session, owner_id, business_id, hour_data)
    finally:
        session.close()
    if result is None:
        logger.warning("could not update busy_hours for business_id=%s owner_id=%s", business_id, owner_id)
    else:
        logger.info("updated busy_hours for business_id=%s", business_id)
    return {"status": "success", "business_id": business_id}

