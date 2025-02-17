from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application Settings."""

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30

    class Config:
        """Config metaclass."""

        env_file = '.env'


settings = Settings()
