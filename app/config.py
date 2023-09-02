from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./database.db"
    REVIEW_LIMIT: int = 30

settings = Settings()
