"""Service layer for Report business logic."""

from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..repository import ReportRepository
from ..models import models


class ReportService:
    """Service class for Report business logic."""

    @staticmethod
    def create_report(
        session: Session,
        business_id: int,
        week_start: datetime,
        week_end: datetime,
        pdf_url: str | None = None,
    ) -> models.Report:
        """Create a new report.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            week_start: Report week start date
            week_end: Report week end date
            pdf_url: PDF URL (optional)
            
        Returns:
            Created Report instance
        """
        return ReportRepository.create_report(session, business_id, week_start, week_end, pdf_url)

    @staticmethod
    def get_business_reports(session: Session, business_id: int) -> List[models.Report]:
        """Get all reports for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of Report instances
        """
        return ReportRepository.get_reports_by_business(session, business_id)

    @staticmethod
    def update_report_pdf_url(
        session: Session, report_id: int, pdf_url: str
    ) -> models.Report | None:
        """Update report PDF URL.
        
        Args:
            session: SQLAlchemy session
            report_id: Report ID
            pdf_url: New PDF URL
            
        Returns:
            Updated Report instance or None if not found
        """
        return ReportRepository.update_report_pdf_url(session, report_id, pdf_url)

    @staticmethod
    def delete_report(session: Session, report_id: int) -> bool:
        """Delete a report.
        
        Args:
            session: SQLAlchemy session
            report_id: Report ID
            
        Returns:
            True if deleted, False if not found
        """
        return ReportRepository.delete_report(session, report_id)
