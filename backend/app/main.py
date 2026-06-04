from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import configuration, health, market_data, scans
from app.core.config import get_settings
from app.core.logging_config import configure_logging


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(
        log_dir=settings.log_dir,
        log_retention_days=settings.log_retention_days,
        log_max_bytes=settings.log_max_bytes,
    )
    app = FastAPI(title="PoorToPour API", version="0.1.0")

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


app = create_app()
