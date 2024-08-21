import logging
import pathlib

import decouple
from pydantic import ConfigDict, BaseConfig
from pydantic_settings import BaseSettings


ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()


class BackendBaseSettings(BaseSettings):
    TITLE: str = "Mastery Backend Version 1.0"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = False

    SERVER_HOST: str = decouple.config("BACKEND_SERVER_HOST", cast=str)  # type: ignore
    SERVER_PORT: int = decouple.config("BACKEND_SERVER_PORT", cast=int)  # type: ignore
    SERVER_WORKERS: int = decouple.config("BACKEND_SERVER_WORKERS", cast=int)  # type: ignore
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    DB_ASYNC_URL: str = decouple.config("DB_ASYNC_URL", cast=str)  # type: ignore

    API_TOKEN: str = decouple.config("API_TOKEN", cast=str)  # type: ignore
    AUTH_TOKEN: str = decouple.config("AUTH_TOKEN", cast=str)  # type: ignore
    JWT_TOKEN_PREFIX: str = decouple.config("JWT_TOKEN_PREFIX", cast=str)  # type: ignore
    JWT_SECRET_KEY: str = decouple.config("JWT_SECRET_KEY", cast=str)  # type: ignore
    JWT_SUBJECT: str = decouple.config("JWT_SUBJECT", cast=str)  # type: ignore
    JWT_MIN: int = decouple.config("JWT_MIN", cast=int)  # type: ignore
    JWT_HOUR: int = decouple.config("JWT_HOUR", cast=int)  # type: ignore
    JWT_DAY: int = decouple.config("JWT_DAY", cast=int)  # type: ignore
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = JWT_MIN * JWT_HOUR * JWT_DAY

    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)  # type: ignore
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # React default port
        "http://0.0.0.0:3000",
        "http://0.0.0.0:8000",
        "http:/localhost:8000",
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    HASHING_ALGORITHM_LAYER_1: str = decouple.config("HASHING_ALGORITHM_LAYER_1", cast=str)  # type: ignore
    HASHING_ALGORITHM_LAYER_2: str = decouple.config("HASHING_ALGORITHM_LAYER_2", cast=str)  # type: ignore
    HASHING_SALT: str = decouple.config("HASHING_SALT", cast=str)  # type: ignore
    JWT_ALGORITHM: str = decouple.config("JWT_ALGORITHM", cast=str)  # type: ignore

    class Config(BaseConfig):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/.env"
        extra = 'allow'
        validate_assignment: bool = True

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }
