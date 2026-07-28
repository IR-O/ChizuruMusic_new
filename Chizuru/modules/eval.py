import io, sys, traceback
from pyrogram import filters
from Chizuru import Chizuru
from config import OWNER_ID

@Chizuru.on_message(filters.command(["eval"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def eval_code(_, message):
    code = " ".join(message.command[1:])
    if not code:
        await message.reply_text("❌ Provide code to evaluate.")
        return
    
    try:
        stdout = io.StringIO()
        sys.stdout = stdout
        exec(code)
        sys.stdout = sys.__stdout__
        output = stdout.getvalue()
        await message.reply_text(f"```\n{output[:4000]}\n```")
    except Exception as e:
        await message.reply_text(f"```\n{traceback.format_exc()[:4000]}\n```")
