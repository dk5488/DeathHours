"""Repository for TrafficReading model database operations."""

from sqlalchemy.orm import Session
from typing import List
from ..models import models
from datetime import datetime


class TrafficReadingRepository:
    """Repository class for TrafficReading entity database operations."""

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
        reading = models.TrafficReading(
            business_id=business_id,
            timestamp=timestamp,
            visitors_estimate=visitors_estimate,
            source=source,
        )
        session.add(reading)
        session.commit()
        session.refresh(reading)
        return reading

    @staticmethod
    def get_traffic_readings_by_business(
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
        return (
            session.query(models.TrafficReading)
            .filter(models.TrafficReading.business_id == business_id)
            .order_by(models.TrafficReading.timestamp.desc())
            .limit(limit)
            .all()
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
        return session.query(models.TrafficReading).filter(
            models.TrafficReading.id == reading_id
        ).first()
