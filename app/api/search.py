from fastapi import APIRouter
from sqlalchemy import select
from app.models.review import Review
from app.schemas.review import DefaultResponse
from app.db.database import database
from app.exceptions.exceptions import NotFoundException
from typing import List

router = APIRouter()


@router.get("/by-alcohol", response_model=List[DefaultResponse], summary="Search reviews by alcohol content",
            description="Returns a list of reviews that have the specified alcohol content.")
async def search_by_alcohol(alcohol: float):
    query = select(Review).where(Review.alcohol == alcohol)
    response = await database.fetch_all(query)

    if not response:
        raise NotFoundException(
            f"Review with {alcohol}% of alcohol not found")

    return response


@router.get("/by-rating", response_model=List[DefaultResponse], summary="Search reviews by rating",
            description="Returns a list of reviews that have the specified rating.")
async def search_by_rating(rating: float):
    query = select(Review).where(Review.rating == rating)
    response = await database.fetch_all(query)

    if not response:
        raise NotFoundException(f"Review with {rating} rating not found")

    return response


@router.get("/by-desc", response_model=List[DefaultResponse], summary="Search reviews by description",
            description="Returns a list of reviews that have the specified keyword in their description.")
async def search_by_desc(desc: str):
    query = select(Review).where(Review.description.ilike(f"%{desc}"))

    response = await database.fetch_all(query)

    if not response:
        raise NotFoundException(f"Review with {desc} in description not found")

    return response
