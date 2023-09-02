from fastapi import APIRouter, Query
from sqlalchemy import insert, update, select, delete
from app.models.review import Review
from app.schemas.review import DeleteResponse, AddUpdateReviewResponse, DefaultResponse
from app.db.database import database
from app.exceptions.exceptions import NotFoundException, BadValue
from typing import List
from datetime import datetime

router = APIRouter()

    
@router.post("/add", response_model=DefaultResponse, summary="Add a new review",
             description="Adds a new review with the provided details.")
async def add_review(name: str, description: str, alcohol: float, rating: float):
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


@router.get("/get/all/", response_model=List[DefaultResponse], summary="Get a list of reviews",
            description="Returns a list of reviews with the specified sorting order and limit.")
async def get_reviews(limit: int, sort_by: str =
                      Query("rating", description="Sort reviews by", enum=["rating", "alcohol", "name"])):

    if sort_by not in ["rating", "alcohol", "name"]:
        raise BadValue(f"Provided bad value in sort_by query")

    order_by_column = getattr(Review, sort_by)
    query = select(Review).order_by(order_by_column).limit(limit)
    response = await database.fetch_all(query)
    return response


@router.get("/get/{review_id}", response_model=DefaultResponse, summary="Get review by ID",
            description="Returns a review with the specified ID.")
async def get_review_by_id(review_id: int):
    query = select(Review).filter(Review.id == review_id)
    response = await database.fetch_one(query)

    if response is None:
        raise NotFoundException(f"Review with ID {review_id} not found")

    return response


@router.get("/get/{name}/", response_model=DefaultResponse, summary="Get review by beer name",
            description="Returns a review with the specified beer name.")
async def get_review_by_beer_name(name: str):
    query = select(Review).where(Review.name == name)
    response = await database.fetch_one(query)

    if not response:
        raise NotFoundException(f"Review with name {name} not found")

    return response


@router.put("/edit/{review_id}/", response_model=DefaultResponse, summary="Edit a review",
            description="Edits an existing review with the provided details.")
async def update_review(review_id: int, name: str, description: str, alcohol: float, rating: float):
    date_format = "%Y-%m-%dT%H:%M:%S"
    date = datetime.now().strftime(date_format)
    query = update(Review).where(Review.id == review_id).values(
        name=name, description=description, alcohol=alcohol, rating=rating, added=date)
    await database.execute(query)
    return {"id": review_id, "name": name, "rating": rating, "alcohol": alcohol, "description": description, "added": date}


@router.delete("/delete/{review_id}/", response_model=DeleteResponse, summary="Delete a review",
               description="Deletes a review with the specified ID.")
async def delete_review(review_id: int):
    query = delete(Review).where(Review.id == review_id)
    affected_rows = await database.execute(query)

    if affected_rows == 0:
        raise NotFoundException(f"Review with ID {review_id} not found")

    return {"message": "Review deleted successfully"}
