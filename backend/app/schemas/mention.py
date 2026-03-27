from pydantic import BaseModel
from datetime import datetime


class MentionCreate(BaseModel):
    company_id: int
    source: str
    source_url: str | None = None
    author: str | None = None
    content: str


class MentionOut(BaseModel):
    id: int
    company_id: int
    source: str
    source_url: str | None
    author: str | None
    content: str
    sentiment: str | None
    mention_type: str | None
    reputation_score: float | None
    ai_summary: str | None
    suggested_response: str | None
    status: str
    collected_at: datetime

    class Config:
        from_attributes = True
