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

LOGGER = logging.getLogger(__name__)


# Main User Account
Chizuru = Client(
    "ChizuruAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)


# Bot Account
bot = Client(
    "ChizuruBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# Voice Chat
pytgcalls = PyTgCalls(Chizuru)


SUDOERS = set()


async def start_services():

    await bot.start()

    await Chizuru.start()

    await pytgcalls.start()

    LOGGER.info(
        "Chizuru Music Bot Started Successfully"
    )


async def stop_services():

    await pytgcalls.stop()

    await Chizuru.stop()

    await bot.stop()


__all__ = [
    "Chizuru",
    "bot",
    "pytgcalls",
    "SUDOERS",
    "start_services",
    "stop_services",
    "LOGGER"
]
