import os
import requests
from pyrogram import filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from Chizuru import Chizuru, pytgcalls
from Chizuru.core.utils import get_audio_stream, put, is_empty, task_done
from pytgcalls import AudioPiped, AudioQuality, AudioParameters, Update

DURATION_LIMIT = 300

@Chizuru.on_message(filters.command(["play"], prefixes=["/", "."]))
async def play(_, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("❌ Provide song name or URL.")
        return
    
    msg = await message.reply_text("⏳ Processing...")
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results:
        await msg.edit_text("❌ No results found.")
        return
    
    link = f"https://youtube.com{results[0]['url_suffix']}"
    title = results[0]['title']
    duration = results[0]['duration']
    
    file_path = await get_audio_stream(link)
    
    if pytgcalls.active_calls:
        position = await put(message.chat.id, file=file_path)
        await msg.edit_text(f"✅ Added to queue at #{position}")
    else:
        await pytgcalls.join_group_call(
            message.chat.id,
            AudioPiped(file_path, AudioParameters.from_quality(AudioQuality.STUDIO))
        )
        await msg.edit_text(f"🎵 Now Playing: {title}")

@Chizuru.on_message(filters.command(["skip"], prefixes=["/", "."]))
async def skip(_, message: Message):
    chat_id = message.chat.id
    task_done(chat_id)
    if is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏭️ Queue empty, leaving.")
    else:
        file = get(chat_id)
        await pytgcalls.change_stream(chat_id, AudioPiped(file["file"]))
        await message.reply_text("⏭️ Skipped.")

@Chizuru.on_message(filters.command(["pause"], prefixes=["/", "."]))
async def pause(_, message: Message):
    await pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("⏸️ Paused.")

@Chizuru.on_message(filters.command(["resume"], prefixes=["/", "."]))
async def resume(_, message: Message):
    await pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("▶️ Resumed.")

@Chizuru.on_message(filters.command(["stop"], prefixes=["/", "."]))
async def stop(_, message: Message):
    await pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("⏹️ Stopped.")

@pytgcalls.on_stream_end()
async def on_stream_end(_, update: Update) -> None:
    chat_id = update.chat_id
    task_done(chat_id)
    if is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
    else:
        file = get(chat_id)
        await pytgcalls.change_stream(chat_id, AudioPiped(file["file"]))
