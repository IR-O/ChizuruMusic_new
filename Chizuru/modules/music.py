from pyrogram import filters
from pyrogram.types import Message

from youtube_search import YoutubeSearch

from Chizuru import Chizuru, pytgcalls

from pytgcalls.types import AudioStream


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
            "❌ Song name do"
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
            "❌ Search failed"
        )


    if not result:

        return await msg.edit_text(
            "❌ Song nahi mili"
        )


    url = (
        "https://youtube.com"
        + result[0]["url_suffix"]
    )


    title = result[0]["title"]


    await msg.edit_text(
        "⬇️ Downloading..."
    )


    # yaha apna downloader function lagao
    # example:
    from Chizuru.core.utils import get_audio_stream

    file = await get_audio_stream(url)


    chat_id = message.chat.id


    await pytgcalls.play(
        chat_id,
        AudioStream(
            file
        )
    )


    await msg.edit_text(
        f"🎵 Playing:\n{title}"
    )
