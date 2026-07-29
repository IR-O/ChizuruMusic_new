import asyncio
import importlib
import logging

from pyrogram import idle

from Chizuru.modules import ALL_MODULES

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)


async def chizuru_boot():
    LOGGER.info("Loading modules...")

    for module in ALL_MODULES:
        try:
            importlib.import_module(f"Chizuru.modules.{module}")
            LOGGER.info("Loaded: %s", module)
        except Exception as e:
            LOGGER.exception("Failed to load module %s: %s", module, e)
            raise

    LOGGER.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    LOGGER.info("✅ Chizuru Music Bot Started Successfully")
    LOGGER.info("✅ All Modules Loaded")
    LOGGER.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    await idle()

    LOGGER.info("Stopping Chizuru Music Bot...")


def main():
    asyncio.run(chizuru_boot())


if __name__ == "__main__":
    main()
