import asyncio
import logging
from pyrogram import Client
from pytgcalls import PyTgCalls
from config import API_ID, API_HASH, BOT_TOKEN, SESSION_STRING

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO
)

Chizuru = Client(
    ":Chizuru:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

userbot = Client(
    ":userbot:",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

pytgcalls = PyTgCalls(userbot)

async def chizuru_music():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await Chizuru.start()
    await userbot.start()
    await pytgcalls.start()
    getme = await Chizuru.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = getme.first_name + (" " + getme.last_name if getme.last_name else "")
    logging.info(f"Bot started as @{BOT_USERNAME}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(chizuru_music())
