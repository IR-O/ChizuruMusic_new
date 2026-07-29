import asyncio
import logging

from pyrogram import Client
from pytgcalls import PyTgCalls

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    SESSION_STRING,
)

logging.basicConfig(
    format="[%(levelname)s %(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

loop = asyncio.get_event_loop()

Chizuru = Client(
    "ChizuruBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

userbot = Client(
    "ChizuruAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)

pytgcalls = PyTgCalls(userbot)

BOT_ID = None
BOT_NAME = None
BOT_USERNAME = None


async def chizuru_music():
    global BOT_ID, BOT_NAME, BOT_USERNAME

    await Chizuru.start()
    logging.info("Bot Client Started.")

    await userbot.start()
    logging.info("Assistant Client Started.")

    await pytgcalls.start()
    logging.info("PyTgCalls Started.")

    me = await Chizuru.get_me()

    BOT_ID = me.id
    BOT_USERNAME = me.username
    BOT_NAME = (
        f"{me.first_name} {me.last_name}"
        if me.last_name
        else me.first_name
    )

    logging.info(f"Bot Name: {BOT_NAME}")
    logging.info(f"Bot Username: @{BOT_USERNAME}")
    logging.info(f"Bot ID: {BOT_ID}")


loop.run_until_complete(chizuru_music())
