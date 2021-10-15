from typing import Callable, Union

import pytest
from fastapi import status
from httpx import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User, UserEdit, UserRead, UserReadWithPermissions

BASE_USER_URL = "http://localhost/users"


@pytest.mark.asyncio
async def test_get_users(async_get: Callable, user: UserRead, admin: UserRead):
    response: Response = await async_get(BASE_USER_URL)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 2

    users_with_permissions = [
        UserReadWithPermissions(**user_obj.dict()) for user_obj in [user, admin]
    ]
    for user_with_permission in users_with_permissions:
        assert user_with_permission in data


@pytest.mark.asyncio
async def test_get_user(async_get: Callable, user: UserRead):
    response: Response = await async_get(f"{BASE_USER_URL}/{user.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    user_with_permissions = UserReadWithPermissions(**user.dict())
    assert data == user_with_permissions.dict()


@pytest.mark.asyncio
async def test_create_user(async_post: Callable, session: AsyncSession):
    email = "bob@mail.com"

    response: Response = await async_post(
        BASE_USER_URL, json={"email": email, "password": "qwerty"}
    )
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["email"] == email
    assert data["is_active"] is True

    result = await session.execute(select(User).where(User.email == email))
    new_user: User = result.scalar_one()
    assert new_user.email == email
    assert new_user.is_active is True


@pytest.mark.asyncio
async def test_create_user_email_in_use(async_post: Callable, user: UserRead):
    response: Response = await async_post(
        BASE_USER_URL, json={"email": user.email, "password": "qwerty"}
    )
    assert response.status_code == status.HTTP_409_CONFLICT

    data = response.json()
    assert data["detail"] == "Email is already in use."


@pytest.mark.asyncio
async def test_patch_user(async_patch: Callable, user: UserRead):
    user_edit_payload = UserEdit(email="new@mail.com", password=None)

    response: Response = await async_patch(
        f"{BASE_USER_URL}/{user.id}", json=user_edit_payload.dict()
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["email"] == user_edit_payload.email


@pytest.mark.asyncio
async def test_delete_user(async_delete: Callable, session: AsyncSession, user: UserRead):
    response: Response = await async_delete(f"{BASE_USER_URL}/{user.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    user_read = UserRead(**user.dict())
    assert data == user_read.dict()

    result = await session.execute(select(User).where(User.email == user.email))
    retrieved_user: Union[User, None] = result.scalar_one_or_none()
    assert retrieved_user is None
