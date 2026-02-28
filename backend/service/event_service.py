"""Service layer for Event business logic."""

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..repository import EventRepository
from ..models import models


class EventService:
    """Service class for Event business logic."""

    @staticmethod
    def create_event(
        session: Session,
        business_id: int,
        name: str,
        start_time: datetime,
        end_time: datetime,
        distance_meters: float,
        impact_score: float,
        raw_data: dict | None = None,
    ) -> models.Event:
        """Create a new event.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            name: Event name
            start_time: Event start time
            end_time: Event end time
            distance_meters: Distance in meters
            impact_score: Impact score
            raw_data: Raw event data (optional)
            
        Returns:
            Created Event instance
        """
        return EventRepository.create_event(
            session, business_id, name, start_time, end_time, distance_meters, impact_score, raw_data
        )

    @staticmethod
    def get_business_events(session: Session, business_id: int) -> List[models.Event]:
        """Get all events for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of Event instances
        """
        return EventRepository.get_events_by_business(session, business_id)

    @staticmethod
    def get_upcoming_events(
        session: Session, business_id: int, now: datetime | None = None
    ) -> List[models.Event]:
        """Get upcoming events for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            now: Current datetime (uses current time if not provided)
            
        Returns:
            List of upcoming Event instances
        """
        if now is None:
            now = datetime.utcnow()
        return EventRepository.get_upcoming_events(session, business_id, now)

    @staticmethod
    def delete_event(session: Session, event_id: int) -> bool:
        """Delete an event.
        
        Args:
            session: SQLAlchemy session
            event_id: Event ID
            
        Returns:
            True if deleted, False if not found
        """
        return EventRepository.delete_event(session, event_id)
