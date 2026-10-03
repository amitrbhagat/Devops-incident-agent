from functools import lru_cache

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file = ".env", extra="ignore")

    app_name: str = "ai-incident-agent"
    environment: str = "local"
    log_level: str = "INFO"
    dry_run: bool = True


@lru_cache 
def get_settings() -> Settings:
    return Settings()
