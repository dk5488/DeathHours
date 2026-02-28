"""Convert database `Business` objects into JSON-friendly dictionaries.

The project predominantly relies on Pydantic for API serialization, but
certain internal helper methods return raw dictionaries so callers don't need
ORM objects. This module centralizes that transformation logic.
"""

from typing import Optional

from ..models import models


def to_dict(business: models.Business) -> dict:
    """Return a plain dictionary representation of a Business model.

    Only includes fields that are relevant to the public API.
    """
    return {
        "id": business.id,
        "owner_id": business.owner_id,
        "google_maps_url": business.google_maps_url,
        "name": business.name,
        "category": business.category,
        "address": business.address,
        "timezone": business.timezone,
        "busy_hours": business.busy_hours or {},
        "created_at": business.created_at.isoformat() if business.created_at else None,
    }
