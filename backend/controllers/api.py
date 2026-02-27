from ..models import models, schemas

from ..utils import auth
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..config import db

router = APIRouter()

# --- authentication helpers ---
@router.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, session: Session = Depends(db.get_db)):
    existing = session.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    u = models.User(
        email=user_in.email,
        hashed_password=auth.get_password_hash(user_in.password),
        created_at=datetime.utcnow(),
    )
    session.add(u)
    session.commit()
    session.refresh(u)
    return u


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(db.get_db)
):
    user = auth.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/businesses", response_model=schemas.BusinessOut)
def create_business(
    business: schemas.BusinessCreate,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = models.Business(
        owner_id=current_user.id,
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
def list_businesses(
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return (
        session.query(models.Business)
        .filter(models.Business.owner_id == current_user.id)
        .all()
    )


@router.get("/businesses/{business_id}", response_model=schemas.BusinessOut)
def get_business(
    business_id: int,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = (
        session.query(models.Business)
        .filter(models.Business.id == business_id, models.Business.owner_id == current_user.id)
        .first()
    )
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return b


@router.post("/businesses/{business_id}/traffic", response_model=schemas.TrafficReading)
def ingest_traffic(
    business_id: int,
    reading: schemas.TrafficReading,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # ensure business exists and belongs to user
    b = (
        session.query(models.Business)
        .filter(models.Business.id == business_id, models.Business.owner_id == current_user.id)
        .first()
    )
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


# --- event endpoints ---
@router.post("/businesses/{business_id}/events", response_model=schemas.EventOut, status_code=status.HTTP_201_CREATED)
def create_event(
    business_id: int,
    event_in: schemas.EventIn,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # verify business belongs to user
    b = (
        session.query(models.Business)
        .filter(models.Business.id == business_id, models.Business.owner_id == current_user.id)
        .first()
    )
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    ev = models.Event(
        business_id=business_id,
        name=event_in.name,
        start_time=event_in.start_time,
        end_time=event_in.end_time,
        distance_meters=event_in.distance_meters,
        impact_score=event_in.impact_score,
        raw_data=event_in.raw_data,
    )
    session.add(ev)
    session.commit()
    session.refresh(ev)
    return ev


@router.get("/businesses/{business_id}/events", response_model=List[schemas.EventOut])
def list_events(
    business_id: int,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # ensure business exists and belongs to user
    b = (
        session.query(models.Business)
        .filter(models.Business.id == business_id, models.Business.owner_id == current_user.id)
        .first()
    )
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return (
        session.query(models.Event)
        .filter(models.Event.business_id == business_id)
        .order_by(models.Event.start_time)
        .all()
    )
