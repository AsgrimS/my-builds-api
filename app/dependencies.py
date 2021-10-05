from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import ALGORITHM, SECRET_KEY, Permissions
from app.database import get_db
from app.models.users import User
from app.security import get_user_by_email, oauth2_scheme


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

    if not (user := get_user_by_email(email, db)):
        raise credentials_exception

    return user


def require_admin(current_user: User = Depends(get_current_user)):
    if not Permissions.admin_permission in [
        permission.name for permission in current_user.permissions
    ]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not have required permission.",
        )
