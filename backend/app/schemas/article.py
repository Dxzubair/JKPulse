from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ArticleCreate(BaseModel):
    title: str
    slug: str
    summary: str
    content: str
    content_type: str
    category_id: int
    organization: Optional[str] = None
    source_url: Optional[str] = None
    official_pdf_url: Optional[str] = None
    application_url: Optional[str] = None

class ArticleResponse(BaseModel):
    id: int
    title: str
    slug: str
    summary: str
    content: str
    content_type: str
    category_id: int
    organization: Optional[str] = None
    source_url: Optional[str] = None
    official_pdf_url: Optional[str] = None
    application_url: Optional[str] = None
    status: str
    is_verified: bool
    published_at: Optional[datetime] = None

    class Config:
        from_attributes = True
