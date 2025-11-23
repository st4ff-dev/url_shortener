from pathlib import Path
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).parent.parent

class Config(BaseSettings):
    DB_URL: SecretStr

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8"
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await Tortoise.init(TORTOISE_ORM)

    yield

    await Tortoise.close_connections()


config = Config()

app = FastAPI(lifespan=lifespan)

TORTOISE_ORM = {
    "connections": {"default": config.DB_URL.get_secret_value()},
    "apps": {
        "models": {
            "models": [
                "app.models.url",
                "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}

