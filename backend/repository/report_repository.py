"""Repository for Report model database operations."""

from sqlalchemy.orm import Session
from typing import List
from ..models import models
from datetime import datetime


class ReportRepository:
    """Repository class for Report entity database operations."""

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
        report = models.Report(
            business_id=business_id,
            generated_at=datetime.utcnow(),
            week_start=week_start,
            week_end=week_end,
            pdf_url=pdf_url,
        )
        session.add(report)
        session.commit()
        session.refresh(report)
        return report

    @staticmethod
    def get_reports_by_business(session: Session, business_id: int) -> List[models.Report]:
        """Get all reports for a business.
        
        Args:
            session: SQLAlchemy session
            business_id: Business ID
            
        Returns:
            List of Report instances
        """
        return (
            session.query(models.Report)
            .filter(models.Report.business_id == business_id)
            .order_by(models.Report.generated_at.desc())
            .all()
        )

    @staticmethod
    def get_report_by_id(session: Session, report_id: int) -> models.Report | None:
        """Get a report by ID.
        
        Args:
            session: SQLAlchemy session
            report_id: Report ID
            
        Returns:
            Report instance or None if not found
        """
        return session.query(models.Report).filter(models.Report.id == report_id).first()

    @staticmethod
    def update_report_pdf_url(session: Session, report_id: int, pdf_url: str) -> models.Report | None:
        """Update report PDF URL.
        
        Args:
            session: SQLAlchemy session
            report_id: Report ID
            pdf_url: New PDF URL
            
        Returns:
            Updated Report instance or None if not found
        """
        report = session.query(models.Report).filter(models.Report.id == report_id).first()
        if report:
            report.pdf_url = pdf_url
            session.commit()
            session.refresh(report)
            return report
        return None

    @staticmethod
    def delete_report(session: Session, report_id: int) -> bool:
        """Delete a report.
        
        Args:
            session: SQLAlchemy session
            report_id: Report ID
            
        Returns:
            True if deleted, False if not found
        """
        report = session.query(models.Report).filter(models.Report.id == report_id).first()
        if report:
            session.delete(report)
            session.commit()
            return True
        return False
