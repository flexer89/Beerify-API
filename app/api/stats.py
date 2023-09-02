from fastapi import APIRouter
from sqlalchemy import func, select, extract
from app.models.review import Review
from app.schemas.review import DefaultResponse, CountReviews, AverageRating
from app.db.database import database
from typing import List

router = APIRouter()


@router.get("/count/", response_model=CountReviews, summary="Get the number of reviews",
            description="Returns the total count of reviews in the database.")
async def count_reviews():
    query = select(func.count()).select_from(Review)
    response = await database.fetch_val(query)
    return {"reviews_amount": response}


@router.get("/average-rating/", response_model=AverageRating, summary="Get the average rating",
            description="Calculates and returns the average rating of all reviews in the database.")
async def average_rating():
    query = select(func.avg(Review.rating)).select_from(Review)
    response = await database.fetch_val(query)
    return {"average_rating": response}


@router.get("/top-rated/{amount}/", response_model=List[DefaultResponse], summary="Get top rated reviews",
            description="Returns the specified number of top rated reviews based on their rating.")
async def top_rated(amount: int):
    query = select(Review).order_by(Review.rating.desc()).limit(amount)
    response = await database.fetch_all(query)
    return response


@router.get("/lowest-rated/{amount}/", response_model=List[DefaultResponse], summary="Get lowest rated reviews",
            description="Returns the specified number of lowest rated reviews based on their rating.")
async def lowest_rated(amount: int):
    query = select(Review).order_by(Review.rating.asc()).limit(amount)
    response = await database.fetch_all(query)
    return response


@router.get("/reviews-by-year/{year}/", response_model=List[DefaultResponse], summary="Get reviews by year",
            description="Returns reviews from specified year.")
async def reviews_by_year(year: int):
    query = select(Review).where(extract("year", Review.added) == year)

    response = await database.fetch_all(query)
    return response


@router.get("/reviews-by-month/{year}/{month}", response_model=List[DefaultResponse], summary="Get reviews by month",
            description="Returns reviews from specified month.")
async def reviews_by_month(year: int, month: int):
    query = select(Review).where(extract("year", Review.added) == year, extract("month", Review.added) == month)

    response = await database.fetch_all(query)
    return response
