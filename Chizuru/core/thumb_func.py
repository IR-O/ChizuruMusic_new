import os
import random
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

def truncate(text):
    words = text.split()
    text1, text2 = "", ""
    for i in words:
        if len(text1) + len(i) < 27:
            text1 += " " + i
        elif len(text2) + len(i) < 25:
            text2 += " " + i
    return [text1.strip(), text2.strip()]

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()
    
    # Cover generation logic
    return "final.png"
