import os
from typing import AsyncGenerator, Callable

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, index=True)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
