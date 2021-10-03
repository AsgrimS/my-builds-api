from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import ALGORITHM, SECRET_KEY
from app.database import get_db
from app.models.users import User
from app.security import get_user, oauth2_scheme


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (email := payload.get("sub")):
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if not (user := get_user(email, db)):
        raise credentials_exception

    return user
