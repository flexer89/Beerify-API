from fastapi import APIRouter
from sqlalchemy import func, select, extract
from app.models.review import Review
from app.db.database import database

router = APIRouter()


@router.get("/count/")
async def count_reviews():
    query = select(func.count()).select_from(Review)
    response = await database.fetch_val(query)
    return {"Reviews amount": response}


@router.get("/average-rating/")
async def average_rating():
    query = select(func.avg(Review.rating)).select_from(Review)
    response = await database.fetch_val(query)
    return {"Average rating": response}


@router.get("/top-rated/{amount}/")
async def top_rated(amount: int):
    query = select(Review).order_by(Review.rating.desc()).limit(amount)
    response = await database.fetch_all(query)
    return response


@router.get("/lowest-rated/{amount}/")
async def lowest_rated(amount: int):
    query = select(Review).order_by(Review.rating.asc()).limit(amount)
    response = await database.fetch_all(query)
    return response


@router.get("/reviews-by-year/{year}/")
async def reviews_by_year(year: int):
    query = select(
        extract("year", Review.added).label("year"),
        func.count().label("review_count")
    ).where(extract("year", Review.added) == year).group_by("year")

    response = await database.fetch_all(query)
    return response


@router.get("/reviews-by-month/{year}/{month}")
async def reviews_by_month(year: int, month: int):
    query = select(
        extract("year", Review.added).label("year"),
        extract("month", Review.added).label("month"),
        func.count().label("review_count")
    ).where(extract("year", Review.added) == year, extract("month", Review.added) == month).group_by("year", "month")

    response = await database.fetch_all(query)
    return response
