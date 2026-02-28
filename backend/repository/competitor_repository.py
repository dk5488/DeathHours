"""Repository for Competitor model database operations."""

from sqlalchemy.orm import Session
from typing import List
from ..models import models
from datetime import datetime


class CompetitorRepository:
    """Repository class for Competitor entity database operations."""

    @staticmethod
    def create_competitor(
        session: Session,
        business_id: int,
        name: str,
        google_maps_url: str,
    ) -> models.Competitor:
        """Create a new competitor entry.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            name: Competitor name
            google_maps_url: Competitor Google Maps URL
            
        Returns:
            Created Competitor instance
        """
        competitor = models.Competitor(
            business_id=business_id,
            name=name,
            google_maps_url=google_maps_url,
            added_at=datetime.utcnow(),
        )
        session.add(competitor)
        session.commit()
        session.refresh(competitor)
        return competitor

    @staticmethod
    def get_competitors_by_business(session: Session, business_id: int) -> List[models.Competitor]:
        """Get all competitors for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of Competitor instances
        """
        return (
            session.query(models.Competitor)
            .filter(models.Competitor.business_id == business_id)
            .order_by(models.Competitor.added_at)
            .all()
        )

    @staticmethod
    def get_competitor_by_id(session: Session, competitor_id: int) -> models.Competitor | None:
        """Get a competitor by ID.
        
        Args:
            session: SQLAlchemy session
            competitor_id: Competitor ID
            
        Returns:
            Competitor instance or None if not found
        """
        return session.query(models.Competitor).filter(models.Competitor.id == competitor_id).first()

    @staticmethod
    def get_competitor_by_business_and_id(
        session: Session, business_id: int, competitor_id: int
    ) -> models.Competitor | None:
        """Get a competitor by business ID and competitor ID.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            competitor_id: Competitor ID
            
        Returns:
            Competitor instance or None if not found
        """
        return (
            session.query(models.Competitor)
            .filter(
                models.Competitor.id == competitor_id,
                models.Competitor.business_id == business_id,
            )
            .first()
        )

    @staticmethod
    def delete_competitor(session: Session, competitor_id: int) -> bool:
        """Delete a competitor.
        
        Args:
            session: SQLAlchemy session
            competitor_id: Competitor ID
            
        Returns:
            True if deleted, False if not found
        """
        competitor = session.query(models.Competitor).filter(
            models.Competitor.id == competitor_id
        ).first()
        if competitor:
            session.delete(competitor)
            session.commit()
            return True
        return False
