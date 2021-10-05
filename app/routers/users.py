from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.users import Permission, User
from app.schemas.users import PermissionSchema, UserCreateSchema, UserEditSchema, UserResponseSchema
from app.security import get_password_hash
from app.utils import get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponseSchema, description="Gets a current user.")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "",
    dependencies=[Depends(require_admin)],
    response_model=list[UserResponseSchema],
    description="Gets a list of all users.",
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post(
    "",
    response_model=UserResponseSchema,
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


@router.patch(
    "/{user_id}",
    dependencies=[Depends(require_admin)],
    response_model=UserResponseSchema,
    description="Modify user.",
)
def edit_user(user_id: int, new_data: UserEditSchema, db: Session = Depends(get_db)):
    user = get_user_by_id(user_id, db)

    for key, value in new_data:
        if value:
            setattr(user, key, value)

    db.commit()
    return user


@router.delete(
    "/{user_id}",
    dependencies=[Depends(require_admin)],
    response_model=UserResponseSchema,
    description="Deletes user.",
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(user_id, db)

    db.delete(user)
    db.commit()
    return user


@router.get(
    "/permissions",
    dependencies=[Depends(require_admin)],
    response_model=list[PermissionSchema],
    description="Gets a list of avaible permissions.",
)
def get_permissions(db: Session = Depends(get_db)):
    permissions = db.query(Permission).all()
    return permissions
