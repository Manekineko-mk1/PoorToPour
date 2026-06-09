from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import configuration, health, market_data, scans
from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.services.scheduled_scan import ScheduledScanService


def create_app(start_scheduler: bool = False) -> FastAPI:
    settings = get_settings()
    configure_logging(
        log_dir=settings.log_dir,
        log_retention_days=settings.log_retention_days,
        log_max_bytes=settings.log_max_bytes,
        log_level=settings.log_level,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        scheduled_scan_service = None
        if start_scheduler and settings.scheduled_scan_enabled:
            scheduled_scan_service = ScheduledScanService(settings)
            scheduled_scan_service.start()
            app.state.scheduled_scan_service = scheduled_scan_service
        try:
            yield
        finally:
            if scheduled_scan_service is not None:
                await scheduled_scan_service.stop()

    app = FastAPI(title="PoorToPour API", version="0.1.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router, prefix="/api")
    app.include_router(configuration.router, prefix="/api")
    app.include_router(market_data.router, prefix="/api")
    app.include_router(scans.router, prefix="/api")
    return app


app = create_app(start_scheduler=True)
