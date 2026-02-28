"""Repository for ActionCard model database operations."""

from sqlalchemy.orm import Session
from typing import List
from ..models import models
from datetime import datetime


class ActionCardRepository:
    """Repository class for ActionCard entity database operations."""

    @staticmethod
    def create_action_card(
        session: Session,
        business_id: int,
        time_window_start: datetime,
        time_window_end: datetime,
        severity: str,
        headline: str,
        copy_text: str,
        completed: bool = False,
    ) -> models.ActionCard:
        """Create a new action card.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            time_window_start: Time window start
            time_window_end: Time window end
            severity: Severity level
            headline: Action headline
            copy_text: Suggested copy text
            completed: Whether action is completed
            
        Returns:
            Created ActionCard instance
        """
        card = models.ActionCard(
            business_id=business_id,
            generated_at=datetime.utcnow(),
            time_window_start=time_window_start,
            time_window_end=time_window_end,
            severity=severity,
            headline=headline,
            copy_text=copy_text,
            completed=completed,
        )
        session.add(card)
        session.commit()
        session.refresh(card)
        return card

    @staticmethod
    def get_action_cards_by_business(session: Session, business_id: int) -> List[models.ActionCard]:
        """Get all action cards for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of ActionCard instances
        """
        return (
            session.query(models.ActionCard)
            .filter(models.ActionCard.business_id == business_id)
            .order_by(models.ActionCard.generated_at.desc())
            .all()
        )

    @staticmethod
    def get_action_card_by_id(session: Session, card_id: int) -> models.ActionCard | None:
        """Get an action card by ID.
        
        Args:
            session: SQLAlchemy session
            card_id: ActionCard ID
            
        Returns:
            ActionCard instance or None if not found
        """
        return session.query(models.ActionCard).filter(models.ActionCard.id == card_id).first()

    @staticmethod
    def update_action_card_completion(
        session: Session, card_id: int, completed: bool
    ) -> models.ActionCard | None:
        """Update action card completion status.
        
        Args:
            session: SQLAlchemy session
            card_id: ActionCard ID
            completed: New completion status
            
        Returns:
            Updated ActionCard instance or None if not found
        """
        card = session.query(models.ActionCard).filter(models.ActionCard.id == card_id).first()
        if card:
            card.completed = completed
            session.commit()
            session.refresh(card)
            return card
        return None

    @staticmethod
    def delete_action_card(session: Session, card_id: int) -> bool:
        """Delete an action card.
        
        Args:
            session: SQLAlchemy session
            card_id: ActionCard ID
            
        Returns:
            True if deleted, False if not found
        """
        card = session.query(models.ActionCard).filter(models.ActionCard.id == card_id).first()
        if card:
            session.delete(card)
            session.commit()
            return True
        return False
