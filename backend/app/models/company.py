from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    keywords = Column(Text, nullable=True)  # JSON list de termos a monitorar
    brand_tone = Column(String(255), default="profissional e cordial")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_collected_at = Column(DateTime, nullable=True)

    mentions = relationship("Mention", back_populates="company")
