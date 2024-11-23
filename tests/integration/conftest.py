import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator

from src.main import app
from src.db import get_db
from tests.conftest import test_session

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = test_session 
    async with AsyncClient(
        transport=ASGITransport(app=app, client=("127.0.0.1", 8000)),
        base_url="http://test",
    ) as client:
        yield client
