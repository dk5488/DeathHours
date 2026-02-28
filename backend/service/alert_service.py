"""Service layer for Alert business logic."""

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..repository import AlertRepository
from ..models import models


class AlertService:
    """Service class for Alert business logic."""

    @staticmethod
    def create_alert(
        session: Session,
        business_id: int,
        threshold_pct: float,
        channels: str,
        sent: bool = False,
        predicted_time: datetime | None = None,
    ) -> models.Alert:
        """Create a new alert.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            threshold_pct: Alert threshold percentage
            channels: Alert channels (comma-separated: "email,sms")
            sent: Whether alert has been sent
            predicted_time: Predicted time for alert (optional)
            
        Returns:
            Created Alert instance
        """
        return AlertRepository.create_alert(
            session, business_id, threshold_pct, channels, sent, predicted_time
        )

    @staticmethod
    def get_business_alerts(session: Session, business_id: int) -> List[models.Alert]:
        """Get all alerts for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of Alert instances
        """
        return AlertRepository.get_alerts_by_business(session, business_id)

    @staticmethod
    def get_unsent_alerts(session: Session, business_id: int) -> List[models.Alert]:
        """Get unsent alerts for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of unsent Alert instances
        """
        return AlertRepository.get_unsent_alerts(session, business_id)

    @staticmethod
    def mark_alert_as_sent(session: Session, alert_id: int) -> models.Alert | None:
        """Mark an alert as sent.
        
        Args:
            session: SQLAlchemy session
            alert_id: Alert ID
            
        Returns:
            Updated Alert instance or None if not found
        """
        return AlertRepository.update_alert_sent_status(session, alert_id, True)

    @staticmethod
    def delete_alert(session: Session, alert_id: int) -> bool:
        """Delete an alert.
        
        Args:
            session: SQLAlchemy session
            alert_id: Alert ID
            
        Returns:
            True if deleted, False if not found
        """
        return AlertRepository.delete_alert(session, alert_id)
