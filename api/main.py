from fastapi import FastAPI

from core.config import get_settings
from core.error_handlers import register_exception_handlers
from routers import health_router, instrument, reagent

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(health_router.router)
app.include_router(instrument.router)
app.include_router(reagent.router)
register_exception_handlers(app)
