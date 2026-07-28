import os, random, requests
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from youtube_search import YoutubeSearch
from Chizuru import Chizuru, userbot, pytgcalls
from Chizuru.core.admin_func import authorized_users
from Chizuru.core.utils import get_audio_stream, get_video_stream, put, is_empty, task_done
from Chizuru.core.thumb_func import generate_cover
from pytgcalls.types import AudioPiped, AudioVideoPiped, AudioQuality, AudioParameters, Update

DURATION_LIMIT = 300
que = {}

@Chizuru.on_message(filters.command(["play", "vplay"], prefixes=["/", "."]))
async def play(_, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("❌ Please provide a song name or URL.")
        return
    
    msg = await message.reply_text("⏳ Processing...")
    is_video = message.command[0] == "vplay"
    
    # YouTube search logic
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results:
        await msg.edit_text("❌ No results found.")
        return
    
    link = f"https://youtube.com{results[0]['url_suffix']}"
    title = results[0]['title'][:40]
    duration = results[0]['duration']
    
    # Generate cover
    await generate_cover(message.from_user.mention, title, results[0]['views'], duration, results[0]['thumbnails'][0])
    
    # Download stream
    if is_video:
        file_path = await get_video_stream(link)
    else:
        file_path = await get_audio_stream(link)
    
    # Join or queue
    if pytgcalls.active_calls:
        position = await put(message.chat.id, file=file_path)
        await message.reply_photo("final.png", caption=f"✅ Added to queue at #{position}")
    else:
        if is_video:
            await pytgcalls.join_group_call(message.chat.id, AudioVideoPiped(file_path))
        else:
            await pytgcalls.join_group_call(message.chat.id, AudioPiped(file_path, AudioParameters.from_quality(AudioQuality.STUDIO)))
        await message.reply_photo("final.png", caption=f"🎵 Now Playing: {title}")
    
    os.remove("final.png")
    await msg.delete()

@Chizuru.on_message(filters.command(["skip"], prefixes=["/", "."]))
@authorized_users
async def skip(_, message: Message):
    chat_id = message.chat.id
    task_done(chat_id)
    if is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏭️ Queue empty, leaving voice chat.")
    else:
        file = get(chat_id)
        await pytgcalls.change_stream(chat_id, AudioPiped(file["file"]))
        await message.reply_text("⏭️ Skipped to next song.")

@Chizuru.on_message(filters.command(["pause"], prefixes=["/", "."]))
@authorized_users
async def pause(_, message: Message):
    chat_id = message.chat.id
    await pytgcalls.pause_stream(chat_id)
    await message.reply_text("⏸️ Paused.")

@Chizuru.on_message(filters.command(["resume"], prefixes=["/", "."]))
@authorized_users
async def resume(_, message: Message):
    chat_id = message.chat.id
    await pytgcalls.resume_stream(chat_id)
    await message.reply_text("▶️ Resumed.")

@Chizuru.on_message(filters.command(["end", "stop"], prefixes=["/", "."]))
@authorized_users
async def stop(_, message: Message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await message.reply_text("⏹️ Stopped.")

@Chizuru.on_message(filters.command(["volume"], prefixes=["/", "."]))
@authorized_users
async def volume(_, message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.reply_text("❌ Usage: /volume [1-200]")
        return
    volume = int(args[1])
    await pytgcalls.change_volume_call(message.chat.id, volume)
    await message.reply_text(f"🔊 Volume set to {volume}%")

@pytgcalls.on_stream_end()
async def on_stream_end(_, update: Update) -> None:
    chat_id = update.chat_id
    task_done(chat_id)
    if is_empty(chat_id):
        await pytgcalls.leave_group_call(chat_id)
    else:
        file = get(chat_id)
        await pytgcalls.change_stream(chat_id, AudioPiped(file["file"]))
