import asyncio
import importlib
import os

from Chizuru import start_services


async def main():

    await start_services()

    modules = [
        f[:-3]
        for f in os.listdir(
            "Chizuru/modules"
        )
        if f.endswith(".py")
        and f != "__init__.py"
    ]

    for module in modules:
        importlib.import_module(
            f"Chizuru.modules.{module}"
        )

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
