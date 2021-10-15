import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.dependencies import get_session
from app.main import app
from app.models.users import User


@pytest.fixture(name="session")
async def session_fixture():
    engine = create_async_engine("postgresql+asyncpg://test:test@localhost:15432/test", future=True)
    metadata = SQLModel.metadata

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore

    async with async_session() as session:
        session: AsyncSession

        for table in reversed(metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

        yield session


@pytest.fixture(name="client")
def client_fixture(session: AsyncSession):
    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    client = AsyncClient(app=app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="async_post")
async def async_post_fixture(client: AsyncClient):
    async def _wrapped(url, **kwargs):
        async with client:
            return await client.post(url, **kwargs)

    return _wrapped


@pytest.fixture(name="async_get")
async def async_get_fixture(client: AsyncClient):
    async def _wrapped(url, **kwargs):
        async with client:
            return await client.get(url, **kwargs)

    return _wrapped


@pytest.fixture(name="async_patch")
async def async_patch_fixture(client: AsyncClient):
    async def _wrapped(url, **kwargs):
        async with client:
            return await client.patch(url, **kwargs)

    return _wrapped


@pytest.fixture(name="async_delete")
async def async_delete_fixture(client: AsyncClient):
    async def _wrapped(url, **kwargs):
        async with client:
            return await client.delete(url, **kwargs)

    return _wrapped


@pytest.fixture(name="user")
async def user_fixture(session: AsyncSession):
    user = User(email="bob@mail.com", password="qwerty")
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest.fixture(name="admin")
async def admin_fixture(session: AsyncSession):
    user = User(email="admin@mail.com", password="qwerty")
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
