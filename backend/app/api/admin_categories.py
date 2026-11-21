from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db import get_db
from backend.app.models.category import Category
from backend.app.core.auth import require_admin

router = APIRouter()

@router.post("/categories")
def create_category(
    name: str,
    slug: str,
    description: str = "",
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin)
):
    existing = db.query(Category).filter(
        (Category.name == name) | (Category.slug == slug)
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Category already exists")

    category = Category(name=name, slug=slug, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)

    return {
        "message": "Category created successfully",
        "id": category.id,
        "name": category.name,
        "slug": category.slug
    }
