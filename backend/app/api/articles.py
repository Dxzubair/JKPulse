from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db import get_db
from backend.app.models.article import Article

router = APIRouter()

@router.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    return (
        db.query(Article)
        .filter(Article.status == "published", Article.is_verified == True)
        .order_by(Article.published_at.desc())
        .all()
    )

@router.get("/articles/{slug}")
def get_article(slug: str, db: Session = Depends(get_db)):
    return (
        db.query(Article)
        .filter(
            Article.slug == slug,
            Article.status == "published",
            Article.is_verified == True
        )
        .first()
    )
