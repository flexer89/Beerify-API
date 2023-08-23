from pydantic import BaseModel
from datetime import datetime


class Review(BaseModel):
    id: int
    name: str
    description: str
    alcohol: float
    rating: float
