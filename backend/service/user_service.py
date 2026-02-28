"""Service layer for User business logic."""

from sqlalchemy.orm import Session
from ..repository import UserRepository
from ..models import models


class UserService:
    """Service class for User business logic."""

    @staticmethod
    def register_user(session: Session, email: str, hashed_password: str) -> models.User | None:
        """Register a new user.
        
        Args:
            session: SQLAlchemy session
            email: User email
            hashed_password: Hashed password
            
        Returns:
            Created User instance or None if email already exists
        """
        if UserRepository.user_exists(session, email):
            return None
        return UserRepository.create_user(session, email, hashed_password)

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> models.User | None:
        """Get a user by email.
        
        Args:
            session: SQLAlchemy session
            email: User email
            
        Returns:
            User instance or None if not found
        """
        return UserRepository.get_user_by_email(session, email)

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> models.User | None:
        """Get a user by ID.
        
        Args:
            session: SQLAlchemy session
            user_id: User ID
            
        Returns:
            User instance or None if not found
        """
        return UserRepository.get_user_by_id(session, user_id)
