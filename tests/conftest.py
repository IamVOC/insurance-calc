import pytest
import pytest_asyncio

from alembic import command
from alembic.config import Config
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from src.config import Config as Settings


async_engine = create_async_engine(
    Settings(_env_file='.test.env').DB.URL, pool_size=10, echo=True, max_overflow=10
)

TestingAsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def test_session():
    connection = await async_engine.connect()
    trans = await connection.begin()
    async_session = TestingAsyncSessionLocal(bind=connection)
    nested = await connection.begin_nested()

    @event.listens_for(async_session.sync_session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested

        if not nested.is_active:
            nested = connection.sync_connection.begin_nested()

    yield async_session

    await trans.rollback()
    await async_session.close()
    await connection.close()


@pytest_asyncio.fixture(scope="function")
async def session():
    async for s in test_session():
        yield s
    

@pytest.fixture(scope='session', autouse=True)
def create_test_database():
    alembic_cfg = Config('alembic.ini')
    command.downgrade(alembic_cfg, 'base')
    command.upgrade(alembic_cfg, 'head')
    yield
    command.downgrade(alembic_cfg, 'base')
