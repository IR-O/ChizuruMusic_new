from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from config import MONGO_URL

mongo = MongoCli(MONGO_URL)
db = mongo.chatsdb

async def get_chats():
    return [chat['chat'] async for chat in db.chats.find()]

async def add_chat(chat):
    if not await db.chats.find_one({"chat": chat}):
        await db.chats.insert_one({"chat": chat})

async def del_chat(chat):
    await db.chats.delete_one({"chat": chat})
