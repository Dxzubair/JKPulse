from fastapi import APIRouter
from backend.app.api.categories import router as categories_router
from backend.app.api.articles import router as articles_router
from backend.app.api.admin_articles import router as admin_articles_router
from backend.app.api.admin_categories import router as admin_categories_router
from backend.app.api.admin_sources import router as admin_sources_router
from backend.app.api.admin_auth import router as admin_auth_router
from backend.app.api.admin_stats import router as admin_stats_router

router = APIRouter()

@router.get("/status")
def api_status():
    return {
        "platform": "JK Pulse",
        "status": "operational",
        "message": "JK Pulse API is ready for development"
    }

router.include_router(categories_router, tags=["Categories"])
router.include_router(articles_router, tags=["Articles"])
router.include_router(admin_auth_router, prefix="/admin/auth", tags=["Admin Authentication"])
router.include_router(admin_articles_router, prefix="/admin", tags=["Admin Articles"])
router.include_router(admin_categories_router, prefix="/admin", tags=["Admin Categories"])
router.include_router(admin_sources_router, prefix="/admin", tags=["Admin Sources"])

router.include_router(admin_stats_router, prefix='/admin', tags=['Admin Statistics'])
