import os
from typing import cast

from dotenv import load_dotenv

load_dotenv()

# POSGTRESSQL
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db}"

# FastAPI
DEBUG_MODE = cast(bool, os.getenv("DEBUG_MODE", False))

# Auth
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)


class Permissions:
    admin_permission = "admin_permission"
