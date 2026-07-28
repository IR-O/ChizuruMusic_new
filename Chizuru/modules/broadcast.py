import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait

from Chizuru import Chizuru
from config import OWNER_ID
from Chizuru.core.mongo import get_users, get_chats


@Chizuru.on_message(
    filters.command(["broadcast"], prefixes=["/", "."])
    & filters.user(OWNER_ID)
)
async def broadcast(_, message):

    if not message.reply_to_message:
        return await message.reply_text(
            "❌ Reply to a message to broadcast."
        )

    status = await message.reply_text(
        "⏳ Broadcasting started..."
    )

    users = await get_users()
    chats = await get_chats()

    success = 0
    failed = 0


    # Users Broadcast
    for user in users:
        try:
            await message.reply_to_message.copy(
                user["_id"] if isinstance(user, dict) else user
            )
            success += 1
            await asyncio.sleep(0.2)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            failed += 1


    # Chats Broadcast
    for chat in chats:
        try:
            await message.reply_to_message.copy(
                chat["_id"] if isinstance(chat, dict) else chat
            )
            success += 1
            await asyncio.sleep(0.2)

        except FloodWait as e:
            await asyncio.sleep(e.value)

        except Exception:
            failed += 1


    await status.edit_text(
        f"""
✅ Broadcast Completed

👤 Success: {success}
❌ Failed: {failed}
"""
    )
