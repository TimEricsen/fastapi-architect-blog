from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import make_url

from anime_app.infrastructure.db.config.models.db import DBConfig


def create_pool(db_config: DBConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(url=make_url(db_config.uri), pool_pre_ping=True)
    pool = async_sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False
    )
    return pool
