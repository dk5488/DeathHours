"""Service layer for Competitor business logic."""

from sqlalchemy.orm import Session
from typing import List
from ..repository import CompetitorRepository
from ..models import models


class CompetitorService:
    """Service class for Competitor business logic."""

    @staticmethod
    def add_competitor(
        session: Session,
        business_id: int,
        name: str,
        google_maps_url: str,
    ) -> models.Competitor:
        """Add a new competitor for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            name: Competitor name
            google_maps_url: Competitor Google Maps URL
            
        Returns:
            Created Competitor instance
        """
        return CompetitorRepository.create_competitor(
            session, business_id, name, google_maps_url
        )

    @staticmethod
    def get_business_competitors(session: Session, business_id: int) -> List[models.Competitor]:
        """Get all competitors for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of Competitor instances
        """
        return CompetitorRepository.get_competitors_by_business(session, business_id)

    @staticmethod
    def get_competitor_by_id_and_business(
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
        return CompetitorRepository.get_competitor_by_business_and_id(
            session, business_id, competitor_id
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
        return CompetitorRepository.delete_competitor(session, competitor_id)
