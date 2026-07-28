import logging

from pyrogram import Client
from pytgcalls import PyTgCalls

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    SESSION_STRING
)


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)


Chizuru = Client(
    "ChizuruBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


assistant = Client(
    "ChizuruAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)


pytgcalls = PyTgCalls(assistant)


SUDOERS = set()


async def start_services():

    await Chizuru.start()

    await assistant.start()

    await pytgcalls.start()

    logging.info(
        "Chizuru Music Bot Started Successfully"
    )
