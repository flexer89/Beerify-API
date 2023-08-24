from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, update, select, delete
from app.models.review import Review
from app.schemas.review import Review as ReviewSchema
from app.db.database import database
from app.exceptions import NotFoundException

router = APIRouter()


@router.post("/add", response_model=ReviewSchema)
async def add_review(name: str, description: str, alcohol: float, rating: float):
    query = insert(Review).values(
        name=name, description=description, alcohol=alcohol, rating=rating)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, "name": name, "rating": rating, "alcohol": alcohol, "description": description}


@router.get("/get/{review_id}")
async def get_review(review_id: int):
    query = select(Review).filter(Review.id == review_id)
    response = await database.fetch_one(query)

    if response is None:
        raise NotFoundException(f"Review with ID {review_id} not found")

    return response


@router.get("/get/{name}/")
async def get_review_by_name(name: str):
    query = select(Review).where(Review.name == name).limit(1)
    response = await database.fetch_all(query)

    if not response:
        raise NotFoundException(f"Review with name {name} not found")

    return response


@router.put("/edit/{review_id}/")
async def update_review(review_id: int, name: str, description: str, alcohol: float, rating: float):
    query = update(Review).where(Review.id == review_id).values(
        name=name, description=description, alcohol=alcohol, rating=rating)
    await database.execute(query)
    return {"id": review_id, "name": name, "rating": rating, "alcohol": alcohol, "description": description}


@router.delete("/delete/{review_id}/")
async def delete_review(review_id: int):
    query = delete(Review).where(Review.id == review_id)
    affected_rows = await database.execute(query)

    if affected_rows == 0:
        raise NotFoundException(f"Review with ID {review_id} not found")

    return {"message": "Review deleted successfully"}
