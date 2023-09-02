from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./database.db"
    REVIEW_LIMIT: int = 30
    ALCOHOL_LIMIT: float = 20.0
    RATING_RANGE: float = 10.0
    DESC_MIN_LEN: int = 5
    DESC_MAX_LEN: int = 250

settings = Settings()
