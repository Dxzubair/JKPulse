from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db import get_db
from backend.app.models.source import Source

router = APIRouter()

@router.get("/sources")
def list_sources(db: Session = Depends(get_db)):
    return db.query(Source).order_by(Source.name).all()

@router.post("/sources")
def create_source(
    name: str,
    website_url: str,
    source_type: str = "website",
    db: Session = Depends(get_db)
):
    existing = db.query(Source).filter(
        Source.website_url == website_url
    ).first()

    if existing:
        raise HTTPException(status_code=409, detail="Source already registered")

    source = Source(
        name=name,
        website_url=website_url,
        source_type=source_type
    )

    db.add(source)
    db.commit()
    db.refresh(source)

    return {"message": "Source registered successfully", "id": source.id}

@router.patch("/sources/{source_id}/monitoring")
def toggle_monitoring(source_id: int, enabled: bool, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    source.monitoring_enabled = enabled
    db.commit()

    return {
        "id": source.id,
        "name": source.name,
        "monitoring_enabled": source.monitoring_enabled
    }

@router.patch("/sources/{source_id}/active")
def toggle_source_active(source_id: int, enabled: bool, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    source.is_active = enabled
    db.commit()

    return {
        "id": source.id,
        "name": source.name,
        "is_active": source.is_active
    }
