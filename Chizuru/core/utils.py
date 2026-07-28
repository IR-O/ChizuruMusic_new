import os
import yt_dlp
from asyncio import Queue, QueueEmpty

DURATION_LIMIT = 300
queues = {}

async def put(chat_id: int, **kwargs) -> int:
    if chat_id not in queues:
        queues[chat_id] = Queue()
    await queues[chat_id].put({**kwargs})
    return queues[chat_id].qsize()

def get(chat_id: int):
    if chat_id in queues:
        try:
            return queues[chat_id].get_nowait()
        except QueueEmpty:
            return None
    return None

def is_empty(chat_id: int) -> bool:
    if chat_id in queues:
        return queues[chat_id].empty()
    return True

def task_done(chat_id: int):
    if chat_id in queues:
        try:
            queues[chat_id].task_done()
        except:
            pass

async def get_audio_stream(link):
    opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
    }
    x = yt_dlp.YoutubeDL(opts)
    info = x.extract_info(link, False)
    audio = os.path.join("downloads", f"{info['id']}.{info['ext']}")
    if os.path.exists(audio):
        return audio
    x.download([link])
    return audio

async def get_video_stream(link):
    opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
    }
    x = yt_dlp.YoutubeDL(opts)
    info = x.extract_info(link, False)
    video = os.path.join("downloads", f"{info['id']}.{info['ext']}")
    if os.path.exists(video):
        return video
    x.download([link])
    return video
