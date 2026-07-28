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


@Chizuru.on_message(
    filters.command(
        ["play"],
        prefixes=["/", "."]
    )
)
async def play(_, message: Message):

    query = " ".join(
        message.command[1:]
    )


    if not query:
        return await message.reply_text(
            "❌ Song name do."
        )


    msg = await message.reply_text(
        "🔎 Searching..."
    )


    results = YoutubeSearch(
        query,
        max_results=1
    ).to_dict()


    if not results:
        return await msg.edit_text(
            "❌ Song nahi mila."
        )


    url = (
        "https://youtube.com"
        + results[0]["url_suffix"]
    )


    title = results[0]["title"]


    await msg.edit_text(
        "🎧 Downloading..."
    )


    file = await get_audio_stream(url)



    await pytgcalls.join_group_call(
        message.chat.id,
        AudioPiped(
            file,
            AudioParameters.from_quality(
                AudioQuality.STUDIO
            )
        )
    )


    await msg.edit_text(
        f"🎵 Playing:\n{title}"
    )



@Chizuru.on_message(
    filters.command(
        ["stop"],
        prefixes=["/", "."]
    )
)
async def stop(_, message: Message):

    await pytgcalls.leave_group_call(
        message.chat.id
    )

    await message.reply_text(
        "⏹ Stopped"
    )



@Chizuru.on_message(
    filters.command(
        ["pause"],
        prefixes=["/", "."]
    )
)
async def pause(_, message: Message):

    await pytgcalls.pause_stream(
        message.chat.id
    )

    await message.reply_text(
        "⏸ Paused"
    )



@Chizuru.on_message(
    filters.command(
        ["resume"],
        prefixes=["/", "."]
    )
)
async def resume(_, message: Message):

    await pytgcalls.resume_stream(
        message.chat.id
    )

    await message.reply_text(
        "▶ Resumed"
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

        song = get(chat_id)

        await pytgcalls.change_stream(
            chat_id,
            AudioPiped(
                song["file"],
                AudioParameters.from_quality(
                    AudioQuality.STUDIO
                )
            )
        )
