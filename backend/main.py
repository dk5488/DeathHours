from fastapi import FastAPI
from .db import init_db

app = FastAPI(title="Dead Hours Dashboard API")


@app.on_event("startup")
async def on_startup():
    init_db()


@app.get("/")
async def root():
    return {"message": "Dead Hours API is running"}
