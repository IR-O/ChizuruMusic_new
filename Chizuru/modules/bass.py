import pydub
from pyrogram import filters
from Chizuru import Chizuru

@Chizuru.on_message(filters.command(["bass"], prefixes=["/", "."]))
async def add_bass(_, message):
    if not message.reply_to_message or not message.reply_to_message.audio:
        await message.reply_text("❌ Reply to an audio file.")
        return
    
    msg = await message.reply_text("⏳ Processing...")
    audio = await message.reply_to_message.download()
    audio_segment = pydub.AudioSegment.from_file(audio)
    enhanced = audio_segment + 10
    enhanced.export("bass.mp3", format="mp3")
    await message.reply_audio("bass.mp3")
    await msg.delete()

@Chizuru.on_message(filters.command(["loudly"], prefixes=["/", "."]))
async def make_louder(_, message):
    if not message.reply_to_message or not message.reply_to_message.audio:
        await message.reply_text("❌ Reply to an audio file.")
        return
    
    msg = await message.reply_text("⏳ Processing...")
    audio = await message.reply_to_message.download()
    audio_segment = pydub.AudioSegment.from_file(audio)
    enhanced = audio_segment + 15
    enhanced.export("loud.mp3", format="mp3")
    await message.reply_audio("loud.mp3")
    await msg.delete()
