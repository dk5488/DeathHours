from fastapi import FastAPI
from .config.db import init_db
from .controllers.api import router as api_router

app = FastAPI(title="Dead Hours Dashboard API")


@app.on_event("startup")
async def on_startup():
    init_db()


app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Dead Hours API is running"}
