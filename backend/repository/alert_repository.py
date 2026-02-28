"""Repository for Alert model database operations."""

from sqlalchemy.orm import Session
from typing import List
from ..models import models
from datetime import datetime


class AlertRepository:
    """Repository class for Alert entity database operations."""

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
        alert = models.Alert(
            business_id=business_id,
            threshold_pct=threshold_pct,
            channels=channels,
            created_at=datetime.utcnow(),
            sent=sent,
            predicted_time=predicted_time,
        )
        session.add(alert)
        session.commit()
        session.refresh(alert)
        return alert

    @staticmethod
    def get_alerts_by_business(session: Session, business_id: int) -> List[models.Alert]:
        """Get all alerts for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of Alert instances
        """
        return (
            session.query(models.Alert)
            .filter(models.Alert.business_id == business_id)
            .order_by(models.Alert.id)
            .all()
        )

    @staticmethod
    def get_alert_by_id(session: Session, alert_id: int) -> models.Alert | None:
        """Get an alert by ID.
        
        Args:
            session: SQLAlchemy session
            alert_id: Alert ID
            
        Returns:
            Alert instance or None if not found
        """
        return session.query(models.Alert).filter(models.Alert.id == alert_id).first()

    @staticmethod
    def get_unsent_alerts(session: Session, business_id: int) -> List[models.Alert]:
        """Get unsent alerts for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of unsent Alert instances
        """
        return (
            session.query(models.Alert)
            .filter(
                models.Alert.business_id == business_id,
                models.Alert.sent == False,
            )
            .all()
        )

    @staticmethod
    def update_alert_sent_status(
        session: Session, alert_id: int, sent: bool
    ) -> models.Alert | None:
        """Update alert sent status.
        
        Args:
            session: SQLAlchemy session
            alert_id: Alert ID
            sent: New sent status
            
        Returns:
            Updated Alert instance or None if not found
        """
        alert = session.query(models.Alert).filter(models.Alert.id == alert_id).first()
        if alert:
            alert.sent = sent
            alert.last_sent = datetime.utcnow() if sent else alert.last_sent
            session.commit()
            session.refresh(alert)
            return alert
        return None

    @staticmethod
    def delete_alert(session: Session, alert_id: int) -> bool:
        """Delete an alert.
        
        Args:
            session: SQLAlchemy session
            alert_id: Alert ID
            
        Returns:
            True if deleted, False if not found
        """
        alert = session.query(models.Alert).filter(models.Alert.id == alert_id).first()
        if alert:
            session.delete(alert)
            session.commit()
            return True
        return False
