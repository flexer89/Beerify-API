from pydantic import BaseModel
from datetime import datetime


class DefaultResponse(BaseModel):
    id: int
    name: str
    description: str
    alcohol: float
    rating: float
    added: datetime
    
    
class DeleteResponse(BaseModel):
    message: str = "Review deleted successfully"
    
    
class AddUpdateReviewResponse(BaseModel):
    id: int
    name: str
    rating: float
    alcohol: float
    description: str
    
    
class CountReviews(BaseModel):
    reviews_amount: int
    
    
class AverageRating(BaseModel):
    average_rating: float
