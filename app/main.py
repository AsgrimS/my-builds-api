from fastapi import FastAPI

from app.routers import users
from app.config import DEBUG_MODE

app = FastAPI(debug=DEBUG_MODE)


app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello!"}
