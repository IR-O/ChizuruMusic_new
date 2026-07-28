import asyncio
import importlib
from pyrogram import idle
from Chizuru import Chizuru, userbot, pytgcalls
from Chizuru.modules import ALL_MODULES

async def start():
    await Chizuru.start()
    await userbot.start()
    await pytgcalls.start()
    for module in ALL_MODULES:
        importlib.import_module(f"Chizuru.modules.{module}")
    print("✅ Bot Started Successfully!")
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start())
