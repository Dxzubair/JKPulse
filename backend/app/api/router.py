from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def api_status():
    return {
        "platform": "JK Pulse",
        "status": "operational",
        "message": "JK Pulse API is ready for development"
    }
