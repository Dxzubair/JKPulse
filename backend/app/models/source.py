from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from backend.app.models.base import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    website_url = Column(Text, nullable=False)
    source_type = Column(String(50), default="website")
    region = Column(String(100), default="Jammu and Kashmir")

    is_active = Column(Boolean, default=True)
    monitoring_enabled = Column(Boolean, default=False)

    last_checked_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
