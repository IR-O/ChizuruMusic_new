import asyncio
import importlib
import os

from Chizuru import start_services


async def main():

    await start_services()


    modules_path = "Chizuru/modules"


    for file in os.listdir(modules_path):

        if (
            file.endswith(".py")
            and file != "__init__.py"
        ):

            module = file[:-3]

            importlib.import_module(
                f"Chizuru.modules.{module}"
            )


    logging_message = (
        "All Modules Loaded Successfully"
    )

    print(logging_message)


    await asyncio.Event().wait()



if __name__ == "__main__":

    asyncio.run(main())
