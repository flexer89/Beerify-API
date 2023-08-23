from fastapi import FastAPI
from app.api.stats import router as stats_router
from app.api.review import router as review_router
from app.db.database import database

app = FastAPI()

app.include_router(stats_router, prefix="/stats", tags=["Statistics"])  
app.include_router(review_router, prefix="/review", tags=["Review"]) 


@app.on_event("startup")
async def startup_db():
    await database.connect()

@app.on_event("shutdown")
async def shutdown_db():
    await database.disconnect()
