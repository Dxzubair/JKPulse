from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from backend.app.db import get_db
from backend.app.models.article import Article
from backend.app.schemas.article import ArticleCreate
from backend.app.core.auth import require_admin

router = APIRouter()

@router.get("/articles")
def list_admin_articles(
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin)
):
    return db.query(Article).order_by(Article.created_at.desc()).all()

@router.post("/articles")
def create_article(
    data: ArticleCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin)
):
    existing = db.query(Article).filter(Article.slug == data.slug).first()
    if existing:
        raise HTTPException(status_code=409, detail="Article slug already exists")

    article = Article(
        **data.model_dump(),
        status="draft",
        is_verified=False
    )
    db.add(article)
    db.commit()
    db.refresh(article)

    return {
        "message": "Draft article created successfully",
        "id": article.id,
        "slug": article.slug,
        "status": article.status
    }

@router.post("/articles/{article_id}/publish")
def publish_article(
    article_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin)
):
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.is_verified = True
    article.status = "published"
    article.published_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(article)

    return {
        "message": "Article verified and published",
        "id": article.id,
        "status": article.status,
        "is_verified": article.is_verified
    }
