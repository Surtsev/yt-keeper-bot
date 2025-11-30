from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import Video, get_session, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield


api = FastAPI(lifespan=lifespan)


@api.get("/videos")
async def get_videos(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Video))
    videos = result.scalars().all()
    return {"videos": [{"id": v.id, "url": v.url} for v in videos]}


@api.post("/videos")
async def add_video(url: str, session: AsyncSession = Depends(get_session)):
    video = Video(url=url)
    session.add(video)
    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=400, detail="Cannot add video, maybe URL are duplicate"
        )
    await session.refresh(video)
    return {"message": "Видео добавлено"}


@api.delete("/videos/{id}")
async def delete_video(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Video).where(Video.id == id))
    video = result.scalars().first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    await session.delete(video)  # Удаляем
    await session.commit()  # Коммитим ПОСЛЕ удаления
    return {"message": "Видео удалено"}
