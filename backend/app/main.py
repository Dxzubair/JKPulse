from fastapi import FastAPI

app = FastAPI(
    title="JK Pulse API",
    description="Backend API for JK Pulse - Jobs, Education, News and Opportunities.",
    version="0.1.0",
)

@app.get("/")
def home():
    return {
        "message": "Welcome to JK Pulse API",
        "status": "running",
        "platform": "JK Pulse"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
