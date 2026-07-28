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
    "Chizuru",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


userbot = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)


pytgcalls = PyTgCalls(userbot)


async def chizuru_music():

    await Chizuru.start()

    await userbot.start()

    await pytgcalls.start()


    me = await Chizuru.get_me()

    logging.info(
        f"Bot Started: @{me.username}"
    )


    await asyncio.Event().wait()



if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        chizuru_music()
    )
