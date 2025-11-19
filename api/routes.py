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


@api.delete("/videos/{id}")
async def delete_video(id: int):
    global videos
    for video in videos:
        if videos[id] == video:
            videos.remove(video)
            return {"message": "Видео успешно удалено."}
    return {"message": "Видео не получилось удалить."}
