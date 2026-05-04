from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SENDGRID_API_KEY: str
    SQLALCHEMY_DATABASE_URL: str
    FROM_EMAIL: str
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 7
REFRESH_SECRET_KEY = "my-super-secret-refresh-token-key"

