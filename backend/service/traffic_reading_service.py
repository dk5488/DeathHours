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
        busyness_score: float | None = None,
        source: str | None = None,
        is_estimated: bool = False,
        day_of_week: int | None = None,
        hour: int | None = None,
        is_busy: bool | None = None,
    ) -> models.TrafficReading:
        """Create a new traffic reading.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            timestamp: Reading timestamp
            busyness_score: Busyness percentage 0-100 (optional)
            source: Data source (optional, e.g. "gemini", "outscraper")
            is_estimated: True if synthetic/expected, False if real data (default False)
            day_of_week: 0=Monday...6=Sunday (optional, derived if not provided)
            hour: Hour of day 0-23 (optional, derived if not provided)
            is_busy: True if this hour is typically busy (optional)
            
        Returns:
            Created TrafficReading instance
        """
        return TrafficReadingRepository.create_traffic_reading(
            session, business_id, timestamp, busyness_score, source, 
            is_estimated, day_of_week, hour, is_busy
        )

    @staticmethod
    def upsert_busy_hours_pattern(
        session: Session,
        business_id: int,
        day_of_week: int,
        hour: int,
        is_busy: bool,
        busyness_score: float,
    ) -> models.TrafficReading:
        """Upsert busy hours pattern data.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            day_of_week: 0=Monday...6=Sunday
            hour: Hour of day 0-23
            is_busy: True if this hour is typically busy
            busyness_score: Expected busyness 0-100 (frequency-based)
            
        Returns:
            Updated or created TrafficReading instance
        """
        return TrafficReadingRepository.upsert_busy_hours_pattern(
            session, business_id, day_of_week, hour, is_busy, busyness_score
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
