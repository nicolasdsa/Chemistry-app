from fastapi import FastAPI

from core.config import get_settings
from routers import health_router

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(health_router.router)
