from fastapi import FastAPI
from backend.app.core.config import APP_NAME, APP_VERSION
from backend.app.api.router import router

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Jobs, education, news and opportunities platform.",
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def home():
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "message": "Welcome to JK Pulse"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
