from fastapi import APIRouter, Query
from sqlalchemy import insert, update, select, delete
from app.models.review import Review
from app.schemas.review import DeleteResponse, DefaultResponse
from app.db.database import database
from app.exceptions.exceptions import NotFoundException, BadValue
from typing import List
from datetime import datetime
from app.config import settings
from app.utils.util import *

router = APIRouter()

    
@router.post("/add", response_model=DefaultResponse, summary="Add a new review",
             description="Adds a new review with the provided details.")
async def add_review(name: str, description: str, alcohol: float, rating: float):
    # Validate data:
    if rating > settings.RATING_RANGE or rating < 0:
        raise BadValue("The provided rating is not valid. Please enter a rating between 0 and 10.0.")
    elif not has_one_decimal_place(rating):
        raise BadValue("The provided rating should have at most one decimal place.")
    
    if alcohol > settings.ALCOHOL_LIMIT or alcohol < 0:
        raise BadValue("The specified alcohol content is not valid. Please provide an alcohol content between 0.0 and 20.0.")
    elif not has_one_decimal_place(alcohol):
        raise BadValue("The provided alcohol amount should have at most one decimal place.")
    
    if len(description) > settings.DESC_MAX_LEN or len(description) < settings.DESC_MIN_LEN:
        raise BadValue("The provided review description is not valid. Please enter a description between 5 and 250 characters in length.")
    
    if len(name) < 0 or len(name) > settings.NAME_MAX_LEN:
        raise BadValue("Beer name exceeds the maximum character limit of 50 characters. Please enter a beer name that is 50 characters or shorter.")
    
    date_format = "%Y-%m-%dT%H:%M:%S"
    query = insert(Review).values(
        name=name, description=description, alcohol=alcohol, rating=rating)
    last_record_id = await database.execute(query)
    return {
        "id": last_record_id, 
        "name": name, 
        "rating": rating, 
        "alcohol": alcohol, 
        "description": description, 
        "added": datetime.now().strftime(date_format)
    }


@router.get("/get/all", response_model=List[DefaultResponse], summary="Get a list of reviews",
            description="Returns a list of reviews with the specified sorting order and limit.")
async def get_reviews(limit: int, sort_by: str =
                      Query("rating", description="Sort reviews by", enum=["rating", "alcohol", "name"])):

    if sort_by not in ["rating", "alcohol", "name"]:
        raise BadValue(f"Provided bad value in sort_by query. Choose one of this: 'rating', 'alcohol' or 'name'")
    
    if limit > settings.REVIEW_LIMIT:
        raise BadValue(f"Exceeded the limit of returned results. The maximum number of results is {settings.REVIEW_LIMIT}.")

    order_by_column = getattr(Review, sort_by)
    query = select(Review).order_by(order_by_column).limit(limit)
    response = await database.fetch_all(query)
    return response


@router.get("/get-by-id/{review_id}", response_model=DefaultResponse, summary="Get review by ID",
            description="Returns a review with the specified ID.")
async def get_review_by_id(review_id: int):
    if review_id < 1:
        raise BadValue("Reviev ID can't be lower than 1.")
    
    query = select(Review).filter(Review.id == review_id)
    response = await database.fetch_one(query)

    if response is None:
        raise NotFoundException(f"Review with ID {review_id} not found")

    return response


@router.get("/get-by-name/{name}", response_model=DefaultResponse, summary="Get review by beer name",
            description="Returns a review with the specified beer name.")
async def get_review_by_beer_name(name: str):
    if len(name) < 0 or len(name) > settings.NAME_MAX_LEN:
        raise BadValue("Beer name exceeds the maximum character limit of 50 characters. Please enter a beer name that is 50 characters or shorter.")
    
    query = select(Review).where(Review.name == name)
    response = await database.fetch_one(query)

    if not response:
        raise NotFoundException(f"Review with name {name} not found")

    return response


@router.put("/edit/{review_id}", response_model=DefaultResponse, summary="Edit a review",
            description="Edits an existing review with the provided details.")
async def update_review(review_id: int, name: str, description: str, alcohol: float, rating: float):
    # Validate data:
    if rating > settings.RATING_RANGE or rating < 0:
        raise BadValue("The provided rating is not valid. Please enter a rating between 0 and 10.0.")
    elif not has_one_decimal_place(rating):
        raise BadValue("The provided rating should have at most one decimal place.")
    
    if alcohol > settings.ALCOHOL_LIMIT or alcohol < 0:
        raise BadValue("The specified alcohol content is not valid. Please provide an alcohol content between 0.0 and 20.0.")
    elif not has_one_decimal_place(alcohol):
        raise BadValue("The provided alcohol amount should have at most one decimal place.")
    
    if len(description) > settings.DESC_MAX_LEN or len(description) < settings.DESC_MIN_LEN:
        raise BadValue("The provided review description is not valid. Please enter a description between 5 and 250 characters in length.")
    
    if len(name) < 0 or len(name) > settings.NAME_MAX_LEN:
        raise BadValue("Beer name exceeds the maximum character limit of 50 characters. Please enter a beer name that is 50 characters or shorter.")
    
    date_format = "%Y-%m-%dT%H:%M:%S"
    date = datetime.now().strftime(date_format)
    query = update(Review).where(Review.id == review_id).values(
        name=name, description=description, alcohol=alcohol, rating=rating, added=date)
    
    response = await database.execute(query)
    if not response:
        raise NotFoundException(f"Review with name {name} not found")
    
    return {"id": review_id, "name": name, "rating": rating, "alcohol": alcohol, "description": description, "added": date}


@router.delete("/delete/{review_id}", response_model=DeleteResponse, summary="Delete a review",
               description="Deletes a review with the specified ID.")
async def delete_review(review_id: int):
    query = delete(Review).where(Review.id == review_id)
    response = await database.execute(query)

    if not response:
        raise NotFoundException(f"Review with ID {review_id} not found")

    return {"message": "Review deleted successfully"}
