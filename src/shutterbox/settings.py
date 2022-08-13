import os
from pathlib import Path
from typing import List, Optional

from pydantic import AnyUrl, BaseSettings


class Settings(BaseSettings):
    in_test: bool = False
    debug: bool = False
    cors_allow_origins: List[str] = []
    cors_allow_headers: List[str] = []
    cors_allow_methods: List[str] = ["GET"]
    project_dir: Path
    app_name: str


PROJECT_DIR = Path(__file__).parent.absolute()

settings = Settings(
    app_name="shutterbox",
    project_dir=PROJECT_DIR,
    cors_allow_origins=["*"],
    cors_allow_headers=["*"],
    cors_allow_methods=["OPTIONS", "GET", "POST"],
)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.getenv("ROOT_LOG_LEVEL", "DEBUG"),
    },
    "loggers": {
        "shutterbox": {
            "handlers": ["console"],
            "level": os.getenv("LOG_LEVEL", "ERROR"),
            "propagate": False,
        },
    },
}
