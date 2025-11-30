from fastapi import FastAPI

from api.core.config import get_settings
from api.routers import health_router

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(health_router.router)
