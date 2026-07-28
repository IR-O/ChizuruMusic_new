import asyncio
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
    format="[%(levelname)s] %(asctime)s - %(name)s: %(message)s",
    level=logging.INFO
)


# Telegram Bot

Chizuru = Client(
    "ChizuruBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# User Account (Assistant)

userbot = Client(
    "ChizuruAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)


# PyTgCalls

pytgcalls = PyTgCalls(
    userbot
)


BOT_ID = None
BOT_NAME = None
BOT_USERNAME = None



async def start():

    global BOT_ID
    global BOT_NAME
    global BOT_USERNAME


    await Chizuru.start()

    await userbot.start()


    await pytgcalls.start()


    me = await Chizuru.get_me()


    BOT_ID = me.id

    BOT_USERNAME = me.username

    BOT_NAME = (
        me.first_name
        + (
            f" {me.last_name}"
            if me.last_name
            else ""
        )
    )


    logging.info(
        f"Bot Started: @{BOT_USERNAME}"
    )


    await asyncio.Event().wait()



async def stop():

    await pytgcalls.stop()

    await userbot.stop()

    await Chizuru.stop()



if __name__ == "__main__":

    asyncio.get_event_loop().run_until_complete(
        start()
    )
