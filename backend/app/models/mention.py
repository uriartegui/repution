from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base


class Mention(Base):
    __tablename__ = "mentions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Origem
    source = Column(String(50), nullable=False)   # google, instagram, twitter, reclame_aqui
    source_url = Column(Text, nullable=True)
    author = Column(String(255), nullable=True)

    # Conteúdo
    content = Column(Text, nullable=False)

    # Classificação IA
    sentiment = Column(String(20), nullable=True)  # positive, neutral, negative
    mention_type = Column(String(20), nullable=True)  # complaint, praise, question, crisis
    reputation_score = Column(Float, nullable=True)
    ai_summary = Column(Text, nullable=True)
    suggested_response = Column(Text, nullable=True)

    # Status
    status = Column(String(20), default="pending")  # pending, responded, ignored

    collected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    company = relationship("Company", back_populates="mentions")
