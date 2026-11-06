from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Selenium RPA Service (PostgreSQL Sequential Worker)"
    DEBUG: bool = False

    # Security
    API_KEY: str = "prod-secret-api-key-replace-me"
    BASIC_AUTH_USERNAME: str = "admin"
    BASIC_AUTH_PASSWORD: str = "strong-admin-password-replace-me"

    # PostgreSQL Connection URL
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/automation_db"

    # Worker Settings
    WORKER_POLL_INTERVAL_SECONDS: int = 5
    TASK_TIMEOUT_SECONDS: int = 1800

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
