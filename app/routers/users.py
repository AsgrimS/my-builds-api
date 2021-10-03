from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.users import UserSchema, UserCreateSchema, PermissionSchema
from app.models.users import User, Permission

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    response_model=list[UserSchema],
    description="Gets a list of all users.",
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users


@router.post(
    "/",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new user.",
)
def create_user(new_user_data: UserCreateSchema, db: Session = Depends(get_db)):
    permissions = db.query(Permission).filter(Permission.name.in_(new_user_data.permissions)).all()

    if db.query(User).filter_by(email=new_user_data.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use.")

    new_user = User(
        email=new_user_data.email,
        password=new_user_data.password,
        permissions=permissions,
    )

    db.add(new_user)
    db.commit()

    return new_user


@router.get(
    "/permissions/",
    response_model=list[PermissionSchema],
    description="Gets a list of avaible permissions.",
)
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()

    return permissions
