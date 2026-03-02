import logging

from ..models import models, schemas

logger = logging.getLogger(__name__)

from ..utils import auth
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..config import db
from ..service import (
    UserService,
    BusinessService,
    TrafficReadingService,
    EventService,
    AlertService,
    ActionCardService,
    ReportService,
    CompetitorService,
)

router = APIRouter()

# --- authentication helpers ---
@router.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, session: Session = Depends(db.get_db)):
    hashed_password = auth.get_password_hash(user_in.password)
    u = UserService.register_user(session, user_in.email, hashed_password)
    if u is None:
        raise HTTPException(status_code=400, detail="Email already registered")
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
    b = BusinessService.create_business(
        session,
        current_user.id,
        str(business.google_maps_url),
        business.name,
        business.category,
    )
    if b is None:
        raise HTTPException(status_code=400, detail="Business URL already exists")
    return b


@router.get("/businesses", response_model=List[schemas.BusinessOut])
def list_businesses(
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    return BusinessService.get_user_businesses(session, current_user.id)


@router.get("/businesses/{business_id}", response_model=schemas.BusinessOut)
def get_business(
    business_id: int,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return b


@router.patch("/businesses/{business_id}/busy_hours", response_model=schemas.BusinessOut)
def update_busy_hours(
    business_id: int,
    payload: schemas.BusyHoursUpdate,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # verify ownership
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    updated = BusinessService.update_business_busy_hours(
        session, current_user.id, business_id, payload.busy_hours
    )
    if updated is None:
        # should never happen because we just checked existence, but keep safe
        raise HTTPException(status_code=500, detail="Unable to update busy hours")
    # return fresh object for Pydantic to serialize
    # reload business from session to include new field
    return BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)


@router.post("/businesses/{business_id}/traffic", response_model=schemas.TrafficReading)
def ingest_traffic(
    business_id: int,
    reading: schemas.TrafficReading,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # ensure business exists and belongs to user
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")

    tr = TrafficReadingService.create_traffic_reading(
        session,
        business_id,
        reading.timestamp,
        reading.visitors_estimate,
        reading.source,
    )
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
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    ev = EventService.create_event(
        session,
        business_id,
        event_in.name,
        event_in.start_time,
        event_in.end_time,
        event_in.distance_meters,
        event_in.impact_score,
        event_in.raw_data,
    )
    return ev


@router.get("/businesses/{business_id}/events", response_model=List[schemas.EventOut])
def list_events(
    business_id: int,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # ensure business exists and belongs to user
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return EventService.get_business_events(session, business_id)


# --- alert endpoints ---
@router.post("/businesses/{business_id}/alerts", response_model=schemas.AlertOut, status_code=status.HTTP_201_CREATED)
def create_alert(
    business_id: int,
    alert_in: schemas.AlertCreate,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    al = AlertService.create_alert(
        session,
        business_id,
        alert_in.threshold_pct,
        ",".join(alert_in.channels),
        False,
    )
    # pydantic schema expects channels list
    al.channels = al.channels.split(",") if al.channels else []
    return al


@router.get("/businesses/{business_id}/alerts", response_model=List[schemas.AlertOut])
def list_alerts(
    business_id: int,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    alerts = AlertService.get_business_alerts(session, business_id)
    # convert channels string back to list since schema expects list
    for a in alerts:
        a.channels = a.channels.split(",") if a.channels else []
    return alerts


# --- action card endpoints ---
@router.post("/businesses/{business_id}/action_cards", response_model=schemas.ActionCardOut, status_code=status.HTTP_201_CREATED)
def create_action_card(
    business_id: int,
    card_in: schemas.ActionCardCreate,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    card = ActionCardService.create_action_card(
        session,
        business_id,
        card_in.time_window_start,
        card_in.time_window_end,
        card_in.severity,
        card_in.headline,
        card_in.copy_text,
    )
    return card


@router.get("/businesses/{business_id}/action_cards", response_model=List[schemas.ActionCardOut])
def list_action_cards(
    business_id: int,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return ActionCardService.get_business_action_cards(session, business_id)


@router.patch("/businesses/{business_id}/action_cards/{card_id}", response_model=schemas.ActionCardOut)
def update_action_card(
    business_id: int,
    card_id: int,
    update: schemas.ActionCardUpdate,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    card = ActionCardService.get_business_action_cards(session, business_id)
    # find matching card
    target = next((c for c in card if c.id == card_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Action card not found")
    updated = ActionCardService.mark_action_card_complete(session, card_id) if update.completed else ActionCardService.mark_action_card_incomplete(session, card_id)
    return updated

# --- busy hours endpoints ---
@router.patch("/businesses/{business_id}/busy_hours", response_model=schemas.BusinessOut)
def update_busy_hours(
    business_id: int,
    payload: schemas.BusyHoursUpdate,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    logger.info("patch busy_hours business=%s owner=%s payload=%s", business_id, current_user.id, payload.busy_hours)
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    result = BusinessService.update_business_busy_hours(
        session, current_user.id, business_id, payload.busy_hours
    )
    # BusinessService returns a raw dict which already contains busy_hours
    return result


# --- report endpoints ---
@router.post("/businesses/{business_id}/reports", response_model=schemas.ReportOut, status_code=status.HTTP_201_CREATED)
def create_report(
    business_id: int,
    report_in: schemas.ReportCreate,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    rep = ReportService.create_report(
        session,
        business_id,
        report_in.week_start,
        report_in.week_end,
        report_in.pdf_url,
    )
    return rep


@router.get("/businesses/{business_id}/reports", response_model=List[schemas.ReportOut])
def list_reports(
    business_id: int,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return ReportService.get_business_reports(session, business_id)


# --- competitor endpoints ---
@router.post("/businesses/{business_id}/competitors", response_model=schemas.CompetitorOut, status_code=status.HTTP_201_CREATED)
def add_competitor(
    business_id: int,
    comp_in: schemas.CompetitorCreate,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    c = CompetitorService.add_competitor(
        session, business_id, comp_in.name, str(comp_in.google_maps_url)
    )
    return c


@router.get("/businesses/{business_id}/competitors", response_model=List[schemas.CompetitorOut])
def list_competitors(
    business_id: int,
    session: Session = Depends(db.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    b = BusinessService.get_business_by_id_and_owner(session, business_id, current_user.id)
    if not b:
        raise HTTPException(status_code=404, detail="Business not found")
    return CompetitorService.get_business_competitors(session, business_id)
