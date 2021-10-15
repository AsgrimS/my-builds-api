from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.users import User


async def get_user_by_email(user_email: str, session: AsyncSession) -> User:
    result = await session.execute(
        select(User).options(joinedload(User.permissions)).where(User.email == user_email)
    )
    if not (user := result.unique().scalar_one_or_none()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    result = await session.execute(
        select(User).options(joinedload(User.permissions)).where(User.id == user_id)
    )
    if not (user := result.unique().scalar_one_or_none()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user
