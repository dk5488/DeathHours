"""Repository for Business model database operations."""

from sqlalchemy.orm import Session
from typing import List
from ..models import models
from datetime import datetime


class BusinessRepository:
    """Repository class for Business entity database operations."""

    @staticmethod
    def create_business(
        session: Session,
        owner_id: int,
        google_maps_url: str,
        name: str,
        category: str,
        address: str | None = None,
        timezone: str | None = None,
    ) -> models.Business:
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
            Created Business instance
        """
        business = models.Business(
            owner_id=owner_id,
            google_maps_url=google_maps_url,
            name=name,
            category=category,
            address=address,
            timezone=timezone,
            created_at=datetime.utcnow(),
        )
        session.add(business)
        session.commit()
        session.refresh(business)
        return business

    @staticmethod
    def get_business_by_id(session: Session, business_id: int) -> models.Business | None:
        """Get a business by ID.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            Business instance or None if not found
        """
        return session.query(models.Business).filter(models.Business.id == business_id).first()

    @staticmethod
    def get_businesses_by_owner(session: Session, owner_id: int) -> List[models.Business]:
        """Get all businesses owned by a user.
        
        Args:
            session: SQLAlchemy session
            owner_id: Owner user ID
            
        Returns:
            List of Business instances
        """
        return session.query(models.Business).filter(models.Business.owner_id == owner_id).all()

    @staticmethod
    def get_business_by_owner_and_id(
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
        return (
            session.query(models.Business)
            .filter(
                models.Business.id == business_id,
                models.Business.owner_id == owner_id,
            )
            .first()
        )

    @staticmethod
    def business_url_exists(session: Session, google_maps_url: str) -> bool:
        """Check if a business URL already exists.
        
        Args:
            session: SQLAlchemy session
            google_maps_url: Google Maps URL
            
        Returns:
            True if URL exists, False otherwise
        """
        return (
            session.query(models.Business)
            .filter(models.Business.google_maps_url == google_maps_url)
            .first()
            is not None
        )
