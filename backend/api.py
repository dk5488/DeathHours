from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from . import models, schemas, db

router = APIRouter()


@router.post("/businesses", response_model=schemas.BusinessOut)
def create_business(business: schemas.BusinessCreate, session: Session = Depends(db.get_db)):
    b = models.Business(
        google_maps_url=str(business.google_maps_url),
        name=business.name,
        category=business.category,
        created_at=datetime.utcnow(),
    )
    session.add(b)
    session.commit()
    session.refresh(b)
    return b


@router.get("/businesses", response_model=List[schemas.BusinessOut])
def list_businesses(session: Session = Depends(db.get_db)):
    return session.query(models.Business).all()


@router.get("/businesses/{business_id}", response_model=schemas.BusinessOut)
def get_business(business_id: int, session: Session = Depends(db.get_db)):
    b = session.query(models.Business).filter(models.Business.id == business_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return b


@router.post("/businesses/{business_id}/traffic", response_model=schemas.TrafficReading)
def ingest_traffic(business_id: int, reading: schemas.TrafficReading, session: Session = Depends(db.get_db)):
    # ensure business exists
    b = session.query(models.Business).filter(models.Business.id == business_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")

    tr = models.TrafficReading(
        business_id=business_id,
        timestamp=reading.timestamp,
        visitors_estimate=reading.visitors_estimate,
        source=reading.source,
    )
    session.add(tr)
    session.commit()
    session.refresh(tr)
    return tr
