"""Main application for the User Service."""

import logging
import logging.config
from contextlib import asynccontextmanager
from typing import Annotated

from ab_core.alembic_auto_migrate.service import AlembicAutoMigrate
from ab_core.database.databases import Database
from ab_core.dependency import Depends, inject
from fastapi import FastAPI

from ab_service.user.routes.user import router as user_router

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {  # root logger
            "level": "INFO",
            "handlers": ["default"],
            "propagate": False,
        },
        "ab_core.alembic_auto_migrate.service": {  # root logger
            "level": "DEBUG",
            "handlers": ["default"],
        },
        "uvicorn.error": {
            "level": "DEBUG",
            "handlers": ["default"],
        },
        "uvicorn.access": {
            "level": "DEBUG",
            "handlers": ["default"],
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)


@inject
@asynccontextmanager
async def lifespan(
    _app: FastAPI,
    _db: Annotated[Database, Depends(Database, persist=True)],  # cold start load db into cache
    alembic_auto_migrate: Annotated[AlembicAutoMigrate, Depends(AlembicAutoMigrate, persist=True)],
):
    """Lifespan context manager to handle startup and shutdown events."""
    alembic_auto_migrate.run()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
