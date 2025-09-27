"""Main application for the User Service."""

import logging
import logging.config
import os
from contextlib import asynccontextmanager
from typing import Annotated

from ab_core.database.databases import Database
from ab_core.dependency import Depends, inject
from fastapi import FastAPI

from ab_service.user.routes.user import router as user_router

ROOT_LEVEL = os.environ.get("PROD", "INFO")

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
            "level": ROOT_LEVEL,  # "INFO",
            "handlers": ["default"],
            "propagate": False,
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
    db: Annotated[Database, Depends(Database, persist=True)],
):
    """Lifespan context manager to handle startup and shutdown events."""
    await db.async_upgrade_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
