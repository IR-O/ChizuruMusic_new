from pyrogram import filters
from Chizuru import Chizuru
from config import OWNER_ID
from Chizuru.core.mongo import get_users, get_chats

@Chizuru.on_message(filters.command(["stats"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def stats(_, message):
    users = len(await get_users())
    chats = len(await get_chats())
    await message.reply_text(f"📊 **Bot Stats**\n\n👤 Users: {users}\n💬 Chats: {chats}")
