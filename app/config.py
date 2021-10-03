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


class Permissions:
    admin_permission = "admin_permission"
