from fastapi import FastAPI

from backend.api.routes import router
from backend.api.analysis import router as analysis_router


app = FastAPI(
    title="AI Resume ATS API",
    description="Backend API for Resume ATS Analysis",
    version="1.0.0",
)

app.include_router(router)
app.include_router(analysis_router)


@app.get("/")
def root():
    return {
        "message": "AI Resume ATS API is running",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }