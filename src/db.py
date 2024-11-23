from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


class Base(DeclarativeBase): ...


engine = create_async_engine(settings.DB.URL)
session = async_sessionmaker(engine)


async def get_db():
    async with session() as s:  # pragma: no cover
        yield s  # pragma: no cover
