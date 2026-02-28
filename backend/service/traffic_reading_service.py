"""Service layer for TrafficReading business logic."""

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..repository import TrafficReadingRepository
from ..models import models


class TrafficReadingService:
    """Service class for TrafficReading business logic."""

    @staticmethod
    def create_traffic_reading(
        session: Session,
        business_id: int,
        timestamp: datetime,
        visitors_estimate: int | None = None,
        source: str | None = None,
    ) -> models.TrafficReading:
        """Create a new traffic reading.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            timestamp: Reading timestamp
            visitors_estimate: Estimated number of visitors (optional)
            source: Data source (optional)
            
        Returns:
            Created TrafficReading instance
        """
        return TrafficReadingRepository.create_traffic_reading(
            session, business_id, timestamp, visitors_estimate, source
        )

    @staticmethod
    def get_business_traffic_readings(
        session: Session, business_id: int, limit: int = 100
    ) -> List[models.TrafficReading]:
        """Get traffic readings for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            limit: Maximum number of results (default 100)
            
        Returns:
            List of TrafficReading instances
        """
        return TrafficReadingRepository.get_traffic_readings_by_business(
            session, business_id, limit
        )

    @staticmethod
    def get_traffic_reading_by_id(session: Session, reading_id: int) -> models.TrafficReading | None:
        """Get a traffic reading by ID.
        
        Args:
            session: SQLAlchemy session
            reading_id: TrafficReading ID
            
        Returns:
            TrafficReading instance or None if not found
        """
        return TrafficReadingRepository.get_traffic_reading_by_id(session, reading_id)
