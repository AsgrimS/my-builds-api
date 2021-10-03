from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.users import Permission, User
from app.schemas.users import PermissionSchema, UserCreateSchema, UserSchema
from app.security import get_password_hash, oauth2_scheme

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserSchema, description="Gets a current user.")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "",
    response_model=list[UserSchema],
    description="Gets a list of all users.",
)
def get_users(db: Session = Depends(get_db), _=Depends(oauth2_scheme)):
    users = db.query(User).all()
    return users


@router.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new user.",
)
def create_user(new_user_data: UserCreateSchema, db: Session = Depends(get_db)):
    permissions = db.query(Permission).filter(Permission.name.in_(new_user_data.permissions)).all()

    if db.query(User).filter_by(email=new_user_data.email).one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use.")

    new_user = User(
        email=new_user_data.email,
        password=get_password_hash(new_user_data.password),
        permissions=permissions,
    )

    db.add(new_user)
    db.commit()
    return new_user


@router.get(
    "/permissions",
    response_model=list[PermissionSchema],
    description="Gets a list of avaible permissions.",
)
def get_permissions(db: Session = Depends(get_db), _=Depends(oauth2_scheme)):
    permissions = db.query(Permission).all()
    return permissions
