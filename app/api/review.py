from fastapi import APIRouter
from sqlalchemy import insert, update, select
from app.models.review import Review
from app.schemas.review import Review as ReviewSchema
from app.db.database import database

router = APIRouter()


@router.post("/add", response_model=ReviewSchema)
async def add_review(name: str, description: str, alcohol: float, rating: float):
    query = insert(Review).values(
        name=name, description=description, alcohol=alcohol, rating=rating)
    last_record_id = await database.execute(query)
    return {"id": last_record_id, "name": name, "rating": rating, "alcohol": alcohol, "description": description}


@router.get("/{review_id}")
async def get_review(review_id: int):
    query = select(Review).filter(Review.id == review_id)
    response = await database.fetch_one(query)
    return response


@router.put("/edit/{review_id}")
async def update_review(review_id: str, name: str, description: str, alcohol: float, rating: float):
    query = update(Review).where(Review.id == review_id).values(
        name=name, description=description, alcohol=alcohol, rating=rating)
    await database.execute(query)
    return {"id": review_id, "name": name, "rating": rating, "alcohol": alcohol, "description": description}
