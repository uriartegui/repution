from pydantic import BaseModel
from datetime import datetime


class CompanyCreate(BaseModel):
    name: str
    slug: str
    keywords: str | None = None
    brand_tone: str = "profissional e cordial"


class CompanyOut(BaseModel):
    id: int
    name: str
    slug: str
    keywords: str | None
    brand_tone: str
    created_at: datetime

    class Config:
        from_attributes = True
