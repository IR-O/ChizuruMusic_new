import os, requests, yt_dlp
from youtube_search import YoutubeSearch
from pyrogram import filters
from Chizuru import Chizuru

@Chizuru.on_message(filters.command(["song"], prefixes=["/", "."]))
async def download_song(_, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("❌ Provide a song name.")
        return
    
    msg = await message.reply_text("⏳ Searching...")
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results:
        await msg.edit_text("❌ No results found.")
        return
    
    link = f"https://youtube.com{results[0]['url_suffix']}"
    title = results[0]['title']
    
    await msg.edit_text("📥 Downloading...")
    opts = {"format": "bestaudio[ext=m4a]", "outtmpl": "%(title)s.%(ext)s", "quiet": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(link, download=True)
        filename = ydl.prepare_filename(info)
    
    await message.reply_audio(filename, title=title, performer=results[0]['channel'])
    os.remove(filename)
    await msg.delete()

@Chizuru.on_message(filters.command(["video"], prefixes=["/", "."]))
async def download_video(_, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("❌ Provide a video name.")
        return
    
    msg = await message.reply_text("⏳ Searching...")
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results:
        await msg.edit_text("❌ No results found.")
        return
    
    link = f"https://youtube.com{results[0]['url_suffix']}"
    title = results[0]['title']
    
    await msg.edit_text("📥 Downloading...")
    opts = {"format": "best", "outtmpl": "%(title)s.%(ext)s", "quiet": True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(link, download=True)
        filename = ydl.prepare_filename(info)
    
    await message.reply_video(filename, caption=title)
    os.remove(filename)
    await msg.delete()
