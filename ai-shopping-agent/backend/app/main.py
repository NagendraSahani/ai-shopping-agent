from fastapi import FastAPI

from app.core.config import settings
from app.core.config import settings

print("Database URL:", settings.DATABASE_URL)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)


@app.get("/")
def home():

    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
    }