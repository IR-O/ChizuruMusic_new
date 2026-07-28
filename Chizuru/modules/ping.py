import time
from pyrogram import filters
from Chizuru import Chizuru

@Chizuru.on_message(filters.command(["ping"], prefixes=["/", "."]))
async def ping(_, message):
    start = time.time()
    msg = await message.reply_text("Pinging...")
    end = time.time()
    await msg.edit_text(f"🏓 **Pong!**\n`{round((end-start)*1000, 2)} ms`")
