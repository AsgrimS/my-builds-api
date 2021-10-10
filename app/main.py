from fastapi import FastAPI

from app.config import DEBUG_MODE
from app.routers import auth, users

app = FastAPI(debug=DEBUG_MODE)

app.include_router(users.router)
app.include_router(auth.router)
