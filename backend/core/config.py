from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"
    groq_timeout: int = 60
    groq_max_retries: int = 3
    kubeconfig_path: str = ""

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
