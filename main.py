from fastapi import FastAPI
from app.api.stats import router as stats_router
from app.api.review import router as review_router
from app.api.search import router as search_router
from app.db.database import database

app = FastAPI(description="Beerify API is a FastAPI-based web application for collecting and managing beer reviews.",            title="Beerify API",
              )

@app.get("/", tags=["Root"])
def root():
    return {
            "health": "OK",
            "openapiapi documentation url":"/docs",
            "redoc documentation url ": "/redoc"
    }

# Include all routers
app.include_router(stats_router, prefix="/stats", tags=["Statistics"])
app.include_router(review_router, prefix="/review", tags=["Review"])
app.include_router(search_router, prefix="/search", tags=["Search"])


@app.on_event("startup")
async def startup_db():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_db():
    await database.disconnect()
