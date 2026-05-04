from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SENDGRID_API_KEY: str
    SQLALCHEMY_DATABASE_URL: str
    FROM_EMAIL: str

    class Config:
        env_file = ".env"

settings = Settings()

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS = 7
REFRESH_SECRET_KEY = "my-super-secret-refresh-token-key"

