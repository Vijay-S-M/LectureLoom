from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "examate-rag"
    environment: str = "local"  # local | ci | production

    # LLM Settings
    primary_model: str = "gpt-4o-mini"
    fallback_model: str = "gpt-3.5-turbo"
    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    fallback_api_key: str = ""
    fallback_base_url: str = "https://api.openai.com/v1"
    llm_timeout_seconds: float = 10.0
    llm_max_retries: int = 2

    # Database & Storage
    database_url: str = "postgresql://postgres:postgres@localhost:5432/lectureloom"
    usage_db_path: str = "data/usage.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()
