from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "AI Intelligence Ingestion"
    environment: str = "development"

    # Crawling
    crawler_concurrency: int = 20
    request_timeout_seconds: int = 30
    max_retries: int = 3

    # LLM
    llm_max_retries: int = 3
    llm_max_input_tokens: int = 12000

    # API keys
    gemini_api_key: str | None = None
    groq_api_key: str | None = None
    deepseek_api_key: str | None = None
    github_token: str | None = None

    # Database
    database_url: str | None = None

    # Redis
    redis_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()