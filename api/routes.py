from fastapi import FastAPI

api = FastAPI()

# Be deprecated soon
videos = []


@api.get("/videos")
async def get_videos():
    return {"videos": videos}


@api.post("/videos")
async def add_video(url: str):
    video = {"id": len(videos) + 1, "url": url}
    videos.append(video)
    return {"message": "Видео добавлено", "video": video}


@api.delete(f"/videos/{id}")
async def delete_video(id: int):
    global videos
    videos = [video for video in videos if video["id"] != id]
    return {"message": "Видео удалено"}
