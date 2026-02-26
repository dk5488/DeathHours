from pydantic import BaseModel, HttpUrl
from typing import Optional

class BusinessCreate(BaseModel):
    google_maps_url: HttpUrl
    name: Optional[str]
    category: Optional[str]

class BusinessOut(BaseModel):
    id: int
    google_maps_url: HttpUrl
    name: Optional[str]
    category: Optional[str]

    class Config:
        orm_mode = True
