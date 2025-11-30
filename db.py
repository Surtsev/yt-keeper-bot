import os
from typing import AsyncGenerator, Callable

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DB_URL = os.getenv("DB_URL")
if DB_URL is None:
    raise ValueError("DB_URL не обьявлена в окружении")

engine = create_async_engine(DB_URL, echo=False)
AsyncSessionLocal: Callable[..., AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
