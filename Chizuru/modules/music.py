import os
import requests

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

from pytgcalls.types import (
    AudioPiped,
    AudioQuality,
    AudioParameters,
    Update
)


DURATION_LIMIT = 300


@Chizuru.on_message(filters.command(["play"], prefixes=["/", "."]))
async def play(_, message: Message):
    query = " ".join(message.command[1:])

    if not query:
        await message.reply_text(
            "❌ Provide song name or YouTube URL."
        )
        return

    msg = await message.reply_text(
        "⏳ Searching song..."
    )

    try:
        results = YoutubeSearch(
            query,
            max_results=1
        ).to_dict()

    except Exception:
        await msg.edit_text(
            "❌ Search failed."
        )
        return


    if not results:
        await msg.edit_text(
            "❌ No results found."
        )
        return


    link = (
        "https://youtube.com"
        + results[0]["url_suffix"]
    )

    title = results[0]["title"]


    await msg.edit_text(
        "🎧 Downloading audio..."
    )


    file_path = await get_audio_stream(link)


    if message.chat.id in pytgcalls.active_calls:

        position = await put(
            message.chat.id,
            file=file_path
        )

        await msg.edit_text(
            f"✅ Added to queue #{position}"
        )

    else:

        await pytgcalls.join_group_call(
            message.chat.id,
            AudioPiped(
                file_path,
                AudioParameters.from_quality(
                    AudioQuality.STUDIO
                )
            )
        )

        await msg.edit_text(
            f"🎵 Now Playing:\n{title}"
        )



@Chizuru.on_message(
    filters.command(
        ["skip", "pause", "resume", "stop"],
        prefixes=["/", "."]
    )
)
async def control(_, message: Message):

    cmd = message.command[0].lower()

    chat_id = message.chat.id


    if cmd == "skip":

        task_done(chat_id)


        if is_empty(chat_id):

            await pytgcalls.leave_group_call(
                chat_id
            )

            await message.reply_text(
                "⏭️ Queue empty."
            )

        else:

            file = get(chat_id)

            await pytgcalls.change_stream(
                chat_id,
                AudioPiped(
                    file["file"],
                    AudioParameters.from_quality(
                        AudioQuality.STUDIO
                    )
                )
            )

            await message.reply_text(
                "⏭️ Skipped."
            )


    elif cmd == "pause":

        await pytgcalls.pause_stream(
            chat_id
        )

        await message.reply_text(
            "⏸️ Paused."
        )


    elif cmd == "resume":

        await pytgcalls.resume_stream(
            chat_id
        )

        await message.reply_text(
            "▶️ Resumed."
        )


    elif cmd == "stop":

        await pytgcalls.leave_group_call(
            chat_id
        )

        await message.reply_text(
            "⏹️ Stopped."
        )



@pytgcalls.on_stream_end()
async def stream_end(
    _,
    update: Update
):

    chat_id = update.chat_id


    task_done(chat_id)


    if is_empty(chat_id):

        await pytgcalls.leave_group_call(
            chat_id
        )

    else:

        file = get(chat_id)

        await pytgcalls.change_stream(
            chat_id,
            AudioPiped(
                file["file"],
                AudioParameters.from_quality(
                    AudioQuality.STUDIO
                )
            )
        )
