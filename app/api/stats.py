from fastapi import APIRouter
from sqlalchemy import func, select, extract
from app.models.review import Review
from app.schemas.review import DefaultResponse, CountReviews, AverageRating
from app.db.database import database
from typing import List
from app.exceptions.exceptions import BadValue
from app.config import settings

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
    if amount > settings.REVIEW_LIMIT:
        raise BadValue(f"Exceeded the limit of returned results. The maximum number of results is {settings.REVIEW_LIMIT}.")
    elif amount < 0:
        raise BadValue("A positive integer is required as the number of results. Please provide a number greater than zero.")
    
    query = select(Review).order_by(Review.rating.desc()).limit(amount)
    response = await database.fetch_all(query)
    return response


@router.get("/lowest-rated/{amount}/", response_model=List[DefaultResponse], summary="Get lowest rated reviews",
            description="Returns the specified number of lowest rated reviews based on their rating.")
async def lowest_rated(amount: int):
    if amount > settings.REVIEW_LIMIT:
        raise BadValue(f"Exceeded the limit of returned results. The maximum number of results is {settings.REVIEW_LIMIT}.")
    elif amount < 0:
        raise BadValue("A positive integer is required as the number of results. Please provide a number greater than zero.")
    
    query = select(Review).order_by(Review.rating.asc()).limit(amount)
    response = await database.fetch_all(query)
    return response


@router.get("/reviews-by-year/{year}/", response_model=List[DefaultResponse], summary="Get reviews by year",
            description="Returns reviews from specified year.")
async def reviews_by_year(year: int):
    if year > 2100 or year < 1900:
        raise BadValue("The specified year is not within the valid range. Please provide a year between 1900 and 2100.")
    
    query = select(Review).where(extract("year", Review.added) == year)
    response = await database.fetch_all(query)
    return response


@router.get("/reviews-by-month/{year}/{month}", response_model=List[DefaultResponse], summary="Get reviews by month",
            description="Returns reviews from specified month.")
async def reviews_by_month(year: int, month: int):
    if year > 2100 or year < 1900:
        raise BadValue("The specified year is not within the valid range. Please provide a year between 1900 and 2100.")
    elif month > 12 or month < 1:
        raise BadValue("The specified month is not valid. Please provide a month between 1 and 12.")
    
    query = select(Review).where(extract("year", Review.added) == year, extract("month", Review.added) == month)
    response = await database.fetch_all(query)
    return response
