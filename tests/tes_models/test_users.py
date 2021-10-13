from typing import Callable

import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_create_user(async_post: Callable):
    response: Response = await async_post(
        "http://localhost/users", json={"email": "Bob", "password": "qwerty"}
    )
    data = response.json()

    assert data["email"] == "Bob"
    assert data["is_active"] == True
