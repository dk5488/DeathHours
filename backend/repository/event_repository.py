"""Repository for Event model database operations."""

from sqlalchemy.orm import Session
from typing import List
from ..models import models
from datetime import datetime


class EventRepository:
    """Repository class for Event entity database operations."""

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
        event = models.Event(
            business_id=business_id,
            name=name,
            start_time=start_time,
            end_time=end_time,
            distance_meters=distance_meters,
            impact_score=impact_score,
            raw_data=raw_data,
        )
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    @staticmethod
    def get_events_by_business(session: Session, business_id: int) -> List[models.Event]:
        """Get all events for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of Event instances
        """
        return (
            session.query(models.Event)
            .filter(models.Event.business_id == business_id)
            .order_by(models.Event.start_time)
            .all()
        )

    @staticmethod
    def get_event_by_id(session: Session, event_id: int) -> models.Event | None:
        """Get an event by ID.
        
        Args:
            session: SQLAlchemy session
            event_id: Event ID
            
        Returns:
            Event instance or None if not found
        """
        return session.query(models.Event).filter(models.Event.id == event_id).first()

    @staticmethod
    def get_upcoming_events(session: Session, business_id: int, now: datetime) -> List[models.Event]:
        """Get upcoming events for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            now: Current datetime for filtering
            
        Returns:
            List of upcoming Event instances
        """
        return (
            session.query(models.Event)
            .filter(
                models.Event.business_id == business_id,
                models.Event.start_time >= now,
            )
            .order_by(models.Event.start_time)
            .all()
        )

    @staticmethod
    def delete_event(session: Session, event_id: int) -> bool:
        """Delete an event.
        
        Args:
            session: SQLAlchemy session
            event_id: Event ID
            
        Returns:
            True if deleted, False if not found
        """
        event = session.query(models.Event).filter(models.Event.id == event_id).first()
        if event:
            session.delete(event)
            session.commit()
            return True
        return False
