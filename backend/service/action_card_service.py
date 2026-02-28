"""Service layer for ActionCard business logic."""

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..repository import ActionCardRepository
from ..models import models


class ActionCardService:
    """Service class for ActionCard business logic."""

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
        return ActionCardRepository.create_action_card(
            session, business_id, time_window_start, time_window_end, severity, headline, copy_text, completed
        )

    @staticmethod
    def get_business_action_cards(session: Session, business_id: int) -> List[models.ActionCard]:
        """Get all action cards for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of ActionCard instances
        """
        return ActionCardRepository.get_action_cards_by_business(session, business_id)

    @staticmethod
    def mark_action_card_complete(session: Session, card_id: int) -> models.ActionCard | None:
        """Mark an action card as complete.
        
        Args:
            session: SQLAlchemy session
            card_id: ActionCard ID
            
        Returns:
            Updated ActionCard instance or None if not found
        """
        return ActionCardRepository.update_action_card_completion(session, card_id, True)

    @staticmethod
    def mark_action_card_incomplete(session: Session, card_id: int) -> models.ActionCard | None:
        """Mark an action card as incomplete.
        
        Args:
            session: SQLAlchemy session
            card_id: ActionCard ID
            
        Returns:
            Updated ActionCard instance or None if not found
        """
        return ActionCardRepository.update_action_card_completion(session, card_id, False)

    @staticmethod
    def delete_action_card(session: Session, card_id: int) -> bool:
        """Delete an action card.
        
        Args:
            session: SQLAlchemy session
            card_id: ActionCard ID
            
        Returns:
            True if deleted, False if not found
        """
        return ActionCardRepository.delete_action_card(session, card_id)
