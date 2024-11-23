import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from sqlalchemy import event, insert
from datetime import date

from src.main import app
from src.db import get_db
from tests.conftest import test_session
from tests.conftest import async_engine, TestingAsyncSessionLocal
from src.tariff.models import Tariff, MaterialRate

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = test_session
    async with AsyncClient(
        transport=ASGITransport(app=app, client=("127.0.0.1", 8000)),
        base_url="http://test",
    ) as client:
        yield client


async def test_insurance_session():
    connection = await async_engine.connect()
    trans = await connection.begin()
    async_session = TestingAsyncSessionLocal(bind=connection)
    nested = await connection.begin_nested()

    @event.listens_for(async_session.sync_session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested

        if not nested.is_active:
            nested = connection.sync_connection.begin_nested()

    raw_res = await async_session.execute(
        insert(Tariff).values([{"relevance_date": date(2020,1,1)}]).returning(Tariff.id)
    )
    tariff_id = raw_res.scalar()
    await async_session.execute(
        insert(MaterialRate).values(
            [{"material_type": "Glass", "rate": 0.3, "tariff_id": tariff_id}]
        )
    )

    yield async_session

    await trans.rollback()
    await async_session.close()
    await connection.close()


@pytest_asyncio.fixture
async def insurance_client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = test_insurance_session
    async with AsyncClient(
        transport=ASGITransport(app=app, client=("127.0.0.1", 8000)),
        base_url="http://test",
    ) as client:
        yield client
