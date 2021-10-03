from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.users import UserSchema, UserCreateSchema
from app.models.users import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("/", response_model=UserSchema)
def create_user(new_user_data: UserCreateSchema, db: Session = Depends(get_db)):
    new_user = User(email=new_user_data.email, password=new_user_data.password)

    db.add(new_user)
    db.commit()

    return new_user
