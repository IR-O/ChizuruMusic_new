import asyncio
from lexica_api import AsyncClient
from pyrogram import filters
from Chizuru import Chizuru

@Chizuru.on_message(filters.command(["gpt", "ai", "bard"], prefixes=["/", "."]))
async def ai_chat(_, message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("❌ Ask me something.")
        return
    
    msg = await message.reply_text("🤔 Thinking...")
    try:
        client = AsyncClient()
        response = await client.ChatCompletion(query, "gpt")
        await msg.edit_text(response['content'][:4000])
    except Exception as e:
        await msg.edit_text(f"❌ Error: {str(e)}")
