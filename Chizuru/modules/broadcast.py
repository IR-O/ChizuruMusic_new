import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from Chizuru import Chizuru
from config import OWNER_ID
from Chizuru.core.mongo import get_users, get_chats

@Chizuru.on_message(filters.command(["broadcast"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def broadcast(_, message):
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a message to broadcast.")
        return
    
    msg = await message.reply_text("⏳ Broadcasting...")
    users = await get_users()
    chats = await get_chats()
    
    success = 0
    failed = 0
    
    for user in users:
        try:
            await message.reply_to_message.copy(user)
            success += 1
            await asyncio.sleep(0.1)
        except:
            failed += 1
    
    for chat in chats:
        try:
            await message.reply_to_message.copy(chat)
            success += 1
            await asyncio.sleep(0.1)
        except:
            failed += 1
    
    await msg.edit_text(f"✅ Broadcast complete!\nSuccess: {success}\nFailed: {failed}")
