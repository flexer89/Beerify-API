from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

# SQLAlchemy Connection Configuration
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

database = Database(DATABASE_URL)
Base.metadata.create_all(bind=engine)