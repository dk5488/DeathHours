from fastapi import FastAPI

app = FastAPI(title="Dead Hours Dashboard API")

@app.get("/")
async def root():
    return {"message": "Dead Hours API is running"}
