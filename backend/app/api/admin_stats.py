from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db import get_db
from backend.app.models.article import Article
from backend.app.models.category import Category
from backend.app.models.source import Source
from backend.app.core.auth import require_admin

router = APIRouter()

@router.get("/stats")
def admin_stats(db: Session = Depends(get_db), username: str = Depends(require_admin)):
    total_articles = db.query(Article).count()
    published_articles = db.query(Article).filter(Article.status == "published").count()
    draft_articles = db.query(Article).filter(Article.status == "draft").count()
    verified_articles = db.query(Article).filter(Article.is_verified == True).count()
    total_categories = db.query(Category).count()
    total_sources = db.query(Source).count()

    return {
        "total_articles": total_articles,
        "published_articles": published_articles,
        "draft_articles": draft_articles,
        "verified_articles": verified_articles,
        "total_categories": total_categories,
        "total_sources": total_sources
    }
