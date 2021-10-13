import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.dependencies import get_session
from app.main import app


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
async def async_post(client: AsyncClient):
    async def _wrapped(url, **kwargs):
        async with client:
            return await client.post(url, **kwargs)

    return _wrapped
