from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional, List, Any
from datetime import datetime

# --- business related ---
class BusinessCreate(BaseModel):
    google_maps_url: HttpUrl
    name: Optional[str]
    category: Optional[str]


# --- user auth ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# --- busy hours update ---
class BusyHoursUpdate(BaseModel):
    busy_hours: dict

    class Config:
        schema_extra = {
            "example": {"busy_hours": {"monday": [1, 2, 3], "tuesday": []}}
        }



class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class BusinessOut(BaseModel):
    id: int
    google_maps_url: HttpUrl
    name: Optional[str]
    category: Optional[str]
    busy_hours: Optional[dict] = None

    class Config:
        orm_mode = True

# --- traffic readings ---
class TrafficReading(BaseModel):
    timestamp: datetime
    visitors_estimate: Optional[int]
    source: Optional[str]

    class Config:
        orm_mode = True

# --- event ---
class EventIn(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    distance_meters: float
    impact_score: float
    raw_data: Any


# --- token models ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None

class EventOut(EventIn):
    id: int

    class Config:
        orm_mode = True

# --- alert ---
class AlertCreate(BaseModel):
    threshold_pct: float
    channels: List[str]

class AlertOut(AlertCreate):
    id: int
    created_at: datetime
    last_sent: Optional[datetime]
    predicted_time: Optional[datetime]
    sent: bool

    class Config:
        orm_mode = True

# --- action card ---
class ActionCardCreate(BaseModel):
    time_window_start: datetime
    time_window_end: datetime
    severity: str
    headline: str
    copy_text: str

class ActionCardOut(ActionCardCreate):
    id: int
    generated_at: datetime
    completed: bool

    class Config:
        orm_mode = True


class ActionCardUpdate(BaseModel):
    completed: bool

# --- report ---
class ReportCreate(BaseModel):
    week_start: datetime
    week_end: datetime
    pdf_url: Optional[HttpUrl]

class ReportOut(ReportCreate):
    id: int
    generated_at: datetime

    class Config:
        orm_mode = True


# --- competitor ---
class CompetitorCreate(BaseModel):
    name: str
    google_maps_url: HttpUrl

class CompetitorOut(CompetitorCreate):
    id: int
    added_at: datetime

    class Config:
        orm_mode = True
