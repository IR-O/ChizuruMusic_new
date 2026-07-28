import asyncio

from pyrogram import filters
from pyrogram.types import Message

from youtube_search import YoutubeSearch

from Chizuru import Chizuru, pytgcalls

from Chizuru.core.utils import (
    get_audio_stream,
    put,
    get,
    is_empty,
    task_done
)

from pytgcalls.types import AudioStream


DURATION_LIMIT = 300


@Chizuru.on_message(
    filters.command(
        ["play"],
        prefixes=["/", "."]
    )
)
async def play(_, message: Message):

    query = " ".join(message.command[1:])

    if not query:
        return await message.reply_text(
            "❌ Song name do."
        )

    msg = await message.reply_text(
        "🔎 Searching..."
    )

    try:
        result = YoutubeSearch(
            query,
            max_results=1
        ).to_dict()

    except Exception:
        return await msg.edit_text(
            "❌ Search error."
        )

    if not result:
        return await msg.edit_text(
            "❌ Song nahi mili."
        )


    link = (
        "https://youtube.com"
        + result[0]["url_suffix"]
    )

    title = result[0]["title"]


    await msg.edit_text(
        "⬇️ Downloading..."
    )


    file_path = await get_audio_stream(link)

    chat_id = message.chat.id


    if chat_id in pytgcalls.calls:

        pos = await put(
            chat_id,
            file=file_path
        )

        return await msg.edit_text(
            f"✅ Queue me add #{pos}"
        )


    await pytgcalls.play(
        chat_id,
        AudioStream(
            file_path
        )
    )


    await msg.edit_text(
        f"🎵 Playing:\n{title}"
    )



@Chizuru.on_message(
    filters.command(
        [
            "pause",
            "resume",
            "skip",
            "stop"
        ],
        prefixes=["/", "."]
    )
)
async def controls(_, message: Message):

    cmd = message.command[0]
    chat_id = message.chat.id


    if cmd == "pause":

        await pytgcalls.pause(chat_id)

        await message.reply_text(
            "⏸️ Paused"
        )


    elif cmd == "resume":

        await pytgcalls.resume(chat_id)

        await message.reply_text(
            "▶️ Resumed"
        )


    elif cmd == "stop":

        await pytgcalls.leave_call(chat_id)

        await message.reply_text(
            "⏹️ Stopped"
        )


    elif cmd == "skip":

        task_done(chat_id)


        if is_empty(chat_id):

            await pytgcalls.leave_call(chat_id)

            return await message.reply_text(
                "Queue empty"
            )


        file = get(chat_id)


        await pytgcalls.play(
            chat_id,
            AudioStream(
                file["file"]
            )
        )


        await message.reply_text(
            "⏭️ Skipped"
        )



@pytgcalls.on_stream_end()
async def stream_end(client, update):

    chat_id = update.chat_id

    task_done(chat_id)


    if is_empty(chat_id):

        await pytgcalls.leave_call(chat_id)

    else:

        file = get(chat_id)

        await pytgcalls.play(
            chat_id,
            AudioStream(
                file["file"]
            )
        )
