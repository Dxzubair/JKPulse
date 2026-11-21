from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db import get_db
from backend.app.models.admin import Admin
from backend.app.schemas.admin import AdminLogin
from backend.app.core.security import verify_password, generate_token

router = APIRouter()

@router.post("/login")
def admin_login(data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(
        Admin.username == data.username,
        Admin.is_active == True
    ).first()

    if not admin or not verify_password(data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "message": "Login successful",
        "username": admin.username,
        "access_token": generate_token(admin.username),
        "token_type": "bearer"
    }
