import pytest
import asyncio
import pytest_asyncio

from fastapi import FastAPI
from datetime import datetime
from httpx import AsyncClient
from passlib.context import CryptContext
from sqlalchemy import insert, delete, select
from alembic.config import Config as AlembicConfig
from typing import Union, Generator, AsyncGenerator
from testcontainers.postgres import PostgresContainer
from alembic.command import upgrade
from sqlalchemy.orm import close_all_sessions, sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from anime_app.api.main_factory import create_app
from anime_app.api.dependencies.db import DBProvider
from anime_app.infrastructure.db.models import Post, Comment, User
from anime_app.api.dependencies.auth import AuthProvider
from anime_app.api.routes import setup_routers
from anime_app.api.dependencies import setup_dependencies
from anime_app.core.utils.exception_handlers import setup_exception_handlers


@pytest.fixture(scope="session")
def build_test_app(pool: sessionmaker) -> FastAPI:
    auth = AuthProvider()

    app = create_app()
    setup_routers(app)
    db = DBProvider(pool=pool)
    setup_dependencies(app, auth, db)
    setup_exception_handlers(app)

    return app


@pytest_asyncio.fixture
async def session(pool: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session_:
        yield session_


@pytest.fixture(scope="session")
def pool(postgres_url: str) -> Generator[sessionmaker, None, None]:
    engine = create_async_engine(url=postgres_url)
    pool_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    yield pool_
    close_all_sessions()


@pytest.fixture(scope='session')
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer('postgres:15-alpine')
    postgres.get_container_host_ip = lambda: 'localhost'
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url().replace('psycopg2', 'asyncpg')
        yield postgres_url_
    finally:
        postgres.stop()


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='function')
async def client(build_test_app: FastAPI):
    async with AsyncClient(app=build_test_app, base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session')
def alembic_config(postgres_url: str) -> AlembicConfig:
    alembic_cfg = AlembicConfig('alembic.ini')
    alembic_cfg.set_main_option(
        'script_location',
        'tests/migrations'
    )
    alembic_cfg.set_main_option('sqlalchemy.url', postgres_url)
    return alembic_cfg


@pytest.fixture(scope='session', autouse=True)
def upgrade_schema_db(alembic_config: AlembicConfig):
    upgrade(alembic_config, 'head')


@pytest_asyncio.fixture(scope='function')
async def create_post_in_database(session: AsyncSession):
    async def create_post_in_database(id: int, title: str, description: str,
                                      author: str, publication_date: datetime):
        await session.execute(insert(Post).values(
            id=id,
            title=title,
            description=description,
            author=author,
            publication_date=publication_date
        ))
        await session.commit()
    return create_post_in_database


@pytest_asyncio.fixture(scope='function')
async def create_comment_in_database(session: AsyncSession):
    async def create_comment_in_database(id: int, text: str, author: str, post_id: int,
                                         time_posted: datetime, answer_to: Union[int, None] = None):
        await session.execute(insert(Comment).values(
            id=id,
            text=text,
            author=author,
            post_id=post_id,
            time_posted=time_posted,
            answer_to=answer_to
        ))
        await session.commit()
    return create_comment_in_database


@pytest_asyncio.fixture(scope='function')
async def create_user_in_database(session: AsyncSession):
    async def create_user_in_database(id: int, username: str, email: str, hashed_password: str,
                                      creation_date: datetime):
        await session.execute(insert(User).values(
            id=id,
            username=username,
            email=email,
            hashed_password=hashed_password,
            creation_date=creation_date
        ))
        await session.commit()
    return create_user_in_database


@pytest_asyncio.fixture(scope='function')
async def create_database_models(user_data, user2_data, create_user_in_database,
                                 post_data, create_post_in_database,
                                 comment_data, create_comment_in_database):
    async def create_database_models():
        await create_user_in_database(**user_data)
        await create_user_in_database(**user2_data)
        await create_post_in_database(**post_data)
        await create_comment_in_database(**comment_data)
    return create_database_models


@pytest_asyncio.fixture(scope='function')
async def delete_post_from_database(session: AsyncSession):
    async def delete_post_from_database(post_id: int):
        await session.execute(delete(Post).where(Post.id == post_id))
        await session.commit()
    return delete_post_from_database


@pytest_asyncio.fixture(scope='function')
async def delete_comment_from_database(session: AsyncSession):
    async def delete_comment_from_database(comment_id: int):
        await session.execute(delete(Comment).where(Comment.id == comment_id))
        await session.commit()
    return delete_comment_from_database


@pytest_asyncio.fixture(scope='function')
async def delete_user_from_database(session: AsyncSession):
    async def delete_user_from_database(user_id: int):
        await session.execute(delete(User).where(User.id == user_id))
        await session.commit()
    return delete_user_from_database


@pytest_asyncio.fixture(scope='function')
async def delete_database_models(delete_user_from_database,
                                 delete_post_from_database,
                                 delete_comment_from_database):
    async def delete_database_models():
        await delete_comment_from_database(1)
        await delete_post_from_database(1)
        await delete_user_from_database(1)
        await delete_user_from_database(2)
    return delete_database_models


@pytest_asyncio.fixture(scope='function')
async def get_post_from_database(session: AsyncSession):
    async def get_post_from_database(post_id: int):
        query = await session.execute(select(Post).where(Post.id == post_id))
        return query.scalar_one_or_none()
    return get_post_from_database


@pytest_asyncio.fixture(scope='function')
async def get_comment_from_database(session: AsyncSession):
    async def get_comment_from_database(comment_id: int):
        query = await session.execute(select(Comment).where(Comment.id == comment_id))
        return query.scalar_one_or_none()
    return get_comment_from_database


@pytest_asyncio.fixture(scope='function')
async def get_user_from_database(session: AsyncSession):
    async def get_user_from_database(user_id: int):
        query = await session.execute(select(User).where(User.id == user_id))
        return query.scalar_one_or_none()
    return get_user_from_database


@pytest.fixture(scope='function')
def post_data():
    return {
        'id': 1,
        'title': 'What about this title?',
        'description': 'My description',
        'author': 'Someone',
        'publication_date': datetime.utcnow()
    }


@pytest.fixture(scope='function')
def comment_data():
    return {
        'id': 1,
        'text': 'My commeeeent',
        'author': 'Someone',
        'post_id': 1,
        'time_posted': datetime.utcnow(),
        'answer_to': None
    }


@pytest.fixture(scope='function')
def user_data():
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    hashed_password = pwd_context.hash('password')
    return {
        'id': 1,
        'username': 'Someone',
        'email': 'myegmail@gmail.com',
        'hashed_password': hashed_password,
        'creation_date': datetime.utcnow()
    }


@pytest.fixture(scope='function')
def user2_data():
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    hashed_password = pwd_context.hash('password2')
    return {
        'id': 2,
        'username': 'SecondOne',
        'email': 'imsecond@gmail.com',
        'hashed_password': hashed_password,
        'creation_date': datetime.utcnow()
    }
