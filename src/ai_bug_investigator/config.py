"""Настройки приложения.

Все настройки агента собраны в одном классе. Значения берутся из переменных
окружения и файла .env. Остальной код получает настройки только через
get_settings() и никогда не читает os.environ напрямую.
"""

from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )

    app_name: str = "AI Bug Investigator"

    environment: Literal["local", "dev", "prod"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    sentry_webhook_secret: SecretStr | None = None
    github_token: SecretStr | None = None


@lru_cache
def get_settings() -> Settings:
    """Возвращает объект настроек.

    lru_cache превращает функцию в «одиночку»: .env читается и проверяется
    один раз при первом вызове, дальше возвращается тот же объект.
    """
    return Settings()
