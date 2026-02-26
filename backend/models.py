from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    created_at = Column(DateTime)

    businesses = relationship("Business", back_populates="owner")

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String)
    google_maps_url = Column(String, unique=True, nullable=False)
    category = Column(String)
    address = Column(String)
    timezone = Column(String)
    created_at = Column(DateTime)

    owner = relationship("User", back_populates="businesses")
    traffic_readings = relationship("TrafficReading", back_populates="business")
    events = relationship("Event", back_populates="business")
    alerts = relationship("Alert", back_populates="business")
    action_cards = relationship("ActionCard", back_populates="business")
    reports = relationship("Report", back_populates="business")
    competitors = relationship("Competitor", back_populates="business")

class TrafficReading(Base):
    __tablename__ = "traffic_readings"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    visitors_estimate = Column(Integer)
    source = Column(String)  # e.g. "outscraper"

    business = relationship("Business", back_populates="traffic_readings")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    distance_meters = Column(Float)
    impact_score = Column(Float)
    raw_data = Column(JSON)

    business = relationship("Business", back_populates="events")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    threshold_pct = Column(Float, nullable=False)  # e.g. traffic drops below X% of peak
    channels = Column(String)  # comma-separated: "email,sms"
    created_at = Column(DateTime)
    last_sent = Column(DateTime)
    predicted_time = Column(DateTime)
    sent = Column(Boolean, default=False)

    business = relationship("Business", back_populates="alerts")

class ActionCard(Base):
    __tablename__ = "action_cards"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    generated_at = Column(DateTime)
    time_window_start = Column(DateTime)
    time_window_end = Column(DateTime)
    severity = Column(String)
    headline = Column(String)
    copy_text = Column(Text)
    completed = Column(Boolean, default=False)

    business = relationship("Business", back_populates="action_cards")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    generated_at = Column(DateTime)
    week_start = Column(DateTime)
    week_end = Column(DateTime)
    pdf_url = Column(String)

    business = relationship("Business", back_populates="reports")

class Competitor(Base):
    __tablename__ = "competitors"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    name = Column(String)
    google_maps_url = Column(String)
    added_at = Column(DateTime)

    business = relationship("Business", back_populates="competitors")
