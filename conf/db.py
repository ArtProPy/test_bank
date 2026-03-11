"""Общие параметры подключения к бд."""

from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from conf.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_SCHEMA, DB_USER

Base = declarative_base(metadata=MetaData(schema=DB_SCHEMA))

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
# todo
print(DATABASE_URL)

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base.metadata.bind = engine


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
