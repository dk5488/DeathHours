"""Service layer for Business business logic."""

import logging

from sqlalchemy.orm import Session
from typing import List
from ..repository import BusinessRepository
from ..models import models

logger = logging.getLogger(__name__)


class BusinessService:
    """Service class for Business business logic."""

    @staticmethod
    def create_business(
        session: Session,
        owner_id: int,
        google_maps_url: str,
        name: str,
        category: str,
        address: str | None = None,
        timezone: str | None = None,
    ) -> models.Business | None:
        """Create a new business.
        
        Args:
            session: SQLAlchemy session
            owner_id: Owner user ID
            google_maps_url: Google Maps URL
            name: Business name
            category: Business category
            address: Business address (optional)
            timezone: Business timezone (optional)
            
        Returns:
            Created Business instance or None if URL already exists
        """
        if BusinessRepository.business_url_exists(session, google_maps_url):
            return None
        return BusinessRepository.create_business(
            session, owner_id, google_maps_url, name, category, address, timezone
        )
    
    @staticmethod
    def update_business_busy_hours(
        session: Session,
        owner_id: int,
        business_id: int,
        busy_hours: dict,
    ) -> dict | None:
        """Wrapper around repository call that enforces ownership and
        returns a JSON-friendly result.

        Returns ``None`` if the business was not found or not owned by the
        specified user.
        """
        logger.debug("update_business_busy_hours called owner=%s business=%s", owner_id, business_id)
        result = BusinessRepository.update_busy_hours(
            session, owner_id, business_id, busy_hours
        )
        if result is None:
            logger.warning("no business found for owner=%s id=%s during busy_hours update", owner_id, business_id)
        else:
            logger.info("busy_hours updated for business_id=%s", business_id)
        return result

    @staticmethod
    def get_business_by_id_and_owner(
        session: Session, business_id: int, owner_id: int
    ) -> models.Business | None:
        """Get a business by ID and owner ID.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            owner_id: Owner user ID
            
        Returns:
            Business instance or None if not found
        """
        return BusinessRepository.get_business_by_owner_and_id(session, business_id, owner_id)

    @staticmethod
    def get_user_businesses(session: Session, owner_id: int) -> List[models.Business]:
        """Get all businesses owned by a user.
        
        Args:
            session: SQLAlchemy session
            owner_id: Owner user ID
            
        Returns:
            List of Business instances
        """
        return BusinessRepository.get_businesses_by_owner(session, owner_id)

    @staticmethod
    def verify_business_ownership(
        session: Session, business_id: int, owner_id: int
    ) -> bool:
        """Verify that a business is owned by a user.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            owner_id: Owner user ID
            
        Returns:
            True if business is owned by user, False otherwise
        """
        business = BusinessRepository.get_business_by_owner_and_id(
            session, business_id, owner_id
        )
        return business is not None

    @staticmethod
    def get_gmaps_uri_from_business(session: Session) -> List[models.Business]:
        """Get the Google Maps URI for a business.
        
        Args:
            session: SQLAlchemy session
        """

        return BusinessRepository.get_all_businesses(session)

