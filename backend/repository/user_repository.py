"""Repository for User model database operations."""

from sqlalchemy.orm import Session
from ..models import models
from datetime import datetime


class UserRepository:
    """Repository class for User entity database operations."""

    @staticmethod
    def create_user(session: Session, email: str, hashed_password: str) -> models.User:
        """Create a new user.
        
        Args:
            session: SQLAlchemy session
            email: User email
            hashed_password: Hashed password
            
        Returns:
            Created User instance
        """
        user = models.User(
            email=email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow(),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> models.User | None:
        """Get a user by email.
        
        Args:
            session: SQLAlchemy session
            email: User email
            
        Returns:
            User instance or None if not found
        """
        return session.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> models.User | None:
        """Get a user by ID.
        
        Args:
            session: SQLAlchemy session
            user_id: User ID
            
        Returns:
            User instance or None if not found
        """
        return session.query(models.User).filter(models.User.id == user_id).first()

    @staticmethod
    def user_exists(session: Session, email: str) -> bool:
        """Check if a user exists by email.
        
        Args:
            session: SQLAlchemy session
            email: User email
            
        Returns:
            True if user exists, False otherwise
        """
        return session.query(models.User).filter(models.User.email == email).first() is not None
