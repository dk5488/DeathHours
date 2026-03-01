"""Repository for TrafficReading model database operations."""

from sqlalchemy.orm import Session
from sqlalchemy import and_
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
            day_of_week: 0=Monday...6=Sunday (optional, derived from timestamp if not provided)
            hour: Hour of day 0-23 (optional, derived from timestamp if not provided)
            is_busy: True if this hour is typically busy (optional)
            
        Returns:
            Created TrafficReading instance
        """
        # Auto-derive day_of_week and hour from timestamp if not provided
        if day_of_week is None:
            day_of_week = timestamp.weekday()  # 0=Monday...6=Sunday
        if hour is None:
            hour = timestamp.hour
        
        reading = models.TrafficReading(
            business_id=business_id,
            timestamp=timestamp,
            busyness_score=busyness_score,
            source=source,
            is_estimated=is_estimated,
            day_of_week=day_of_week,
            hour=hour,
            is_busy=is_busy,
        )
        session.add(reading)
        session.commit()
        session.refresh(reading)
        return reading

    @staticmethod
    def upsert_busy_hours_pattern(
        session: Session,
        business_id: int,
        day_of_week: int,
        hour: int,
        is_busy: bool,
        busyness_score: float,
        synthetic_timestamp: datetime | None = None,
    ) -> models.TrafficReading:
        """Upsert busy hours pattern data (for expected/typical hours).
        
        Creates or updates pattern data for a specific day/hour combination.
        Used when storing the expected busy pattern from Gemini API.
        
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
        # Find existing pattern entry for this day/hour/business
        existing = session.query(models.TrafficReading).filter(
            and_(
                models.TrafficReading.business_id == business_id,
                models.TrafficReading.day_of_week == day_of_week,
                models.TrafficReading.hour == hour,
                models.TrafficReading.is_estimated == True,
                models.TrafficReading.source == "gemini"
            )
        ).first()
        
        if existing:
            # Update existing pattern
            existing.is_busy = is_busy
            existing.busyness_score = busyness_score
            session.commit()
            session.refresh(existing)
            return existing
        
        # Use provided synthetic timestamp if given, otherwise fall back to an
        # arbitrary informational timestamp (no business timezone context).
        if synthetic_timestamp is None:
            synthetic_timestamp = datetime(2024, 3, 4, hour=hour)

        return TrafficReadingRepository.create_traffic_reading(
            session=session,
            business_id=business_id,
            timestamp=synthetic_timestamp,
            busyness_score=busyness_score,
            source="gemini",
            is_estimated=True,
            day_of_week=day_of_week,
            hour=hour,
            is_busy=is_busy,
        )

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
