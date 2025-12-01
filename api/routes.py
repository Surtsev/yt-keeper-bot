from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func, select, update
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
    return {"videos": [{"#": v.position, "url": v.url} for v in videos]}


@api.post("/videos")
async def add_video(url: str, session: AsyncSession = Depends(get_session)):
    current_position = await session.execute(
        select(func.max(Video.position)).select_from(Video)
    )
    current_position = current_position.scalar()
    new_position = current_position + 1 if current_position is not None else 1
    video = Video(url=url, position=new_position)
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


@api.delete("/videos/{pos}")
async def delete_video(pos: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Video).where(Video.position == pos))
    video = result.scalars().first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    await session.delete(video)

    await session.execute(
        update(Video).where(Video.position > pos).values(position=Video.position - 1)
    )

    await session.commit()
    return {"message": "Видео удалено"}
