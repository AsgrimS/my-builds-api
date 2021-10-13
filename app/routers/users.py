from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_session
from app.dependencies import get_current_user, require_admin
from app.models.users import User, UserCreate, UserEdit, UserRead, UserReadWithPermissions
from app.security import get_password_hash
from app.utils import get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserReadWithPermissions, description="Gets a current user.")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "",
    response_model=list[UserReadWithPermissions],
    description="Gets a list of all users.",
)
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).options(joinedload(User.permissions)))
    users = result.unique().scalars().all()
    return users


@router.get(
    "/{user_id}",
    response_model=UserReadWithPermissions,
    description="Gets a specific user.",
)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_id(user_id, session)
    return user


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new user.",
)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await session.execute(select(User).where(User.email == user_data.email))
    if user.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already in use.")

    new_user = User(email=user_data.email, password=get_password_hash(user_data.password))

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.patch(
    "/{user_id}",
    dependencies=[Depends(require_admin)],
    response_model=UserRead,
    description="Modify user.",
)
async def edit_user(
    user_id: int, user_data: UserEdit, session: AsyncSession = Depends(get_session)
):
    user = await get_user_by_id(user_id, session)

    for key, value in user_data:
        if value:
            setattr(user, key, value)
    await session.commit()

    return user


@router.delete(
    "/{user_id}",
    response_model=UserRead,
    description="Deletes user.",
)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_id(user_id, session)

    await session.delete(user)
    await session.commit()

    return user


@router.get("/hello/hello")
async def read_root():
    return {"Hello": "World"}
