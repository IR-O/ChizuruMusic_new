from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Chizuru import Chizuru
from Chizuru.core.strings import *

buttons = [
    [InlineKeyboardButton("🎵 Music", callback_data="music_"), InlineKeyboardButton("🤖 AI", callback_data="ai_")],
    [InlineKeyboardButton("🔊 Bass", callback_data="bass_"), InlineKeyboardButton("📥 YouTube", callback_data="youtube_")],
    [InlineKeyboardButton("📊 Misc", callback_data="misc_"), InlineKeyboardButton("📢 Broadcast", callback_data="broadcast_")],
    [InlineKeyboardButton("👨‍💻 Devs", callback_data="devs_"), InlineKeyboardButton("📸 Instagram", callback_data="instagram_")],
    [InlineKeyboardButton("❌ Close", callback_data="close_data")]
]

@Chizuru.on_message(filters.command(["help", "start"], prefixes=["/", "."]))
async def help_command(_, message):
    await message.reply_text(help_txt, reply_markup=InlineKeyboardMarkup(buttons))

@Chizuru.on_callback_query()
async def callback_handler(_, query: CallbackQuery):
    data = query.data
    texts = {
        "music_": music_txt, "ai_": ai_txt, "bass_": bass_txt,
        "youtube_": youtube_txt, "misc_": misc_txt, "broadcast_": broadcast_txt,
        "devs_": devs_txt, "instagram_": instagram_txt
    }
    if data in texts:
        await query.edit_message_text(texts[data], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data="help_")]]))
    elif data == "help_":
        await query.edit_message_text(help_txt, reply_markup=InlineKeyboardMarkup(buttons))
    elif data == "close_data":
        await query.message.delete()
