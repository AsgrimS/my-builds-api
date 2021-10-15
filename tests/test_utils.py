import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserRead
from app.utils import get_user_by_email, get_user_by_id


@pytest.mark.asyncio
async def test_get_user_by_email(user: UserRead, session: AsyncSession):
    result_user = await get_user_by_email(user.email, session)
    assert result_user == user


@pytest.mark.asyncio
async def test_get_user_by_email_user_not_found(session: AsyncSession):
    with pytest.raises(HTTPException) as exception:
        await get_user_by_email("bob@mail.com", session)

    assert exception.value.status_code == status.HTTP_404_NOT_FOUND
    assert exception.value.detail == "User not found."


@pytest.mark.asyncio
async def test_get_user_by_id(user: UserRead, session: AsyncSession):
    result_user = await get_user_by_id(user.id, session)
    assert result_user == user


@pytest.mark.asyncio
async def test_get_user_by_id_user_not_found(session: AsyncSession):
    with pytest.raises(HTTPException) as exception:
        await get_user_by_id(1, session)

    assert exception.value.status_code == status.HTTP_404_NOT_FOUND
    assert exception.value.detail == "User not found."
