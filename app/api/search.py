from fastapi import APIRouter
from sqlalchemy import select
from app.models.review import Review
from app.db.database import database
from app.exceptions.exceptions import NotFoundException

router = APIRouter()


@router.get("/by-alcohol")
async def search_by_alcohol(alcohol: float):
    query = select(Review).where(Review.alcohol == alcohol)
    response = await database.fetch_all(query)

    if response == None:
        raise NotFoundException(
            f"Review with f{alcohol}% of alcohol not found")

    return response


@router.get("/by-rating")
async def search_by_rating(rating: float):
    query = select(Review).where(Review.rating == rating)
    response = await database.fetch_all(query)

    if response == None:
        raise NotFoundException(f"Review with {rating} rating not found")

    return response


@router.get("/by-desc")
async def search_by_desc(desc: str):
    query = select(Review).where(Review.description.ilike(f"%{desc}"))

    response = await database.fetch_all(query)

    if response == None:
        raise NotFoundException(f"Review with {desc} in description not found")

    return response
