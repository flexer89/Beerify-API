from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.db.database import Base

class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    rating = Column(Float)
    alcohol = Column(Float)
    description = Column(String)
    added = Column(DateTime, default=func.now(), server_default=func.now())
