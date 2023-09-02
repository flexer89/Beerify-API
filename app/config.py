from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./database.db"
    REVIEW_LIMIT: int = 30
    ALCOHOL_LIMIT: float = 20.0
    RATING_RANGE: float = 10.0
    DESC_MIN_LEN: int = 5
    DESC_MAX_LEN: int = 250
    YEAR_MIN_VALUE: int = 1900
    YEAR_MAX_VALUE: int = 2100
    NAME_MAX_LEN: int = 50

settings = Settings()
