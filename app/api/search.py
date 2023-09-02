from fastapi import APIRouter
from sqlalchemy import select
from app.models.review import Review
from app.schemas.review import DefaultResponse
from app.db.database import database
from app.exceptions.exceptions import NotFoundException, BadValue
from typing import List
from app.config import settings

router = APIRouter()


@router.get("/by-alcohol", response_model=List[DefaultResponse], summary="Search reviews by alcohol content",
            description="Returns a list of reviews that have the specified alcohol content.")
async def search_by_alcohol(alcohol: float):
    if alcohol > settings.ALCOHOL_LIMIT or alcohol < 0:
        raise BadValue("The specified alcohol content is not valid. Please provide an alcohol content between 0.0 and 20.0.")
    elif alcohol % 0.1 != 0:
        raise BadValue("The provided alcohol amount should have at most one decimal place.")
    
    query = select(Review).where(Review.alcohol == alcohol)
    response = await database.fetch_all(query)

    if not response:
        raise NotFoundException(
            f"Review with {alcohol}% of alcohol not found")

    return response


@router.get("/by-rating", response_model=List[DefaultResponse], summary="Search reviews by rating",
            description="Returns a list of reviews that have the specified rating.")
async def search_by_rating(rating: float):
    if rating > settings.RATING_RANGE or rating < 0:
        raise BadValue("The provided rating is not valid. Please enter a rating between 0 and 10.0.")
    elif rating % 0.1 != 0:
        raise BadValue("The provided rating should have at most one decimal place.")
    
    query = select(Review).where(Review.rating == rating)
    response = await database.fetch_all(query)

    if not response:
        raise NotFoundException(f"Review with {rating} rating not found")

    return response


@router.get("/by-desc", response_model=List[DefaultResponse], summary="Search reviews by description",
            description="Returns a list of reviews that have the specified keyword in their description.")
async def search_by_desc(desc: str):
    if len(desc) > settings.DESC_MAX_LEN or len(desc) < settings.DESC_MIN_LEN:
        raise BadValue("The provided review description is not valid. Please enter a description between 5 and 250 characters in length.")
    
    query = select(Review).where(Review.description.ilike(f"%{desc}"))
    response = await database.fetch_all(query)

    if not response:
        raise NotFoundException(f"Review with {desc} in description not found")

    return response
