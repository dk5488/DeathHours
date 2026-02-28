"""Service layer for Business business logic."""

from sqlalchemy.orm import Session
from typing import List
from ..repository import BusinessRepository
from ..models import models


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
