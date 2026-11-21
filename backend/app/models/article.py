from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.app.models.base import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(350), unique=True, nullable=False, index=True)
    summary = Column(Text, nullable=False)
    content = Column(Text, nullable=False)

    content_type = Column(String(50), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    organization = Column(String(250))
    source_url = Column(Text)
    official_pdf_url = Column(Text)
    application_url = Column(Text)

    status = Column(String(30), default="draft", index=True)
    is_verified = Column(Boolean, default=False)

    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
