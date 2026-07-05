from fastapi import FastAPI
from app.database.base import Base
from app.database.connection import engine

from app.models.user import User

from app.core.config import settings
from app.core.config import settings

print("Database URL:", settings.DATABASE_URL)

Base.metadata.create_all(bind=engine)
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