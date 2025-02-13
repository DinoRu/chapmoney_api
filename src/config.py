from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the application."""
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    DOMAIN: str

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')


Config = Settings()





