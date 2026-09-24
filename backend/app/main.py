from fastapi import FastAPI

app = FastAPI(
    title="FinTrack API",
    description="Personal Finance Tracker API",
    version="0.1.0",
)
#app=Fastapi() -- creates application, @app.get("/") - defines a route for the root endpoint, which returns a welcome message and status. The /health endpoint checks the health of the application and returns a status of "healthy".

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