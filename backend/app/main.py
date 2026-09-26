from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title="FinTrack API",
    description="Personal Finance Tracker API",
    version="0.1.0",
)

app.include_router(api_v1_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to FinTrack API",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
    }