from pathlib import Path
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import redis.asyncio as redis
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
    redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="myapp-cache")

    await Tortoise.init(TORTOISE_ORM)

    yield

    await Tortoise.close_connections()


config = Config()

app = FastAPI(lifespan=lifespan)

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {"file_path": config.DB_URL.get_secret_value()} ,
            "minsize": 10,        # минимальное количество соединений в пуле
            "maxsize": 50,        # максимальное количество соединений в пуле
            "timeout": 20,        # таймаут соединения в секундах
        }
    },
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

