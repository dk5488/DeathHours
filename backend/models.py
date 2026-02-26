from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String)
    created_at = Column(DateTime)

class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    google_maps_url = Column(String, unique=True)
    category = Column(String)
    address = Column(String)
    timezone = Column(String)

# additional tables to follow...