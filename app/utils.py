from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.users import User


def get_user_by_email(email: str, db: Session) -> User:
    if not (user := db.query(User).filter_by(email=email).one_or_none()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist.")
    return user


def get_user_by_id(id: int, db: Session) -> User:
    if not (user := db.query(User).get(id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist.")
    return user
