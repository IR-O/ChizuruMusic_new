from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from config import MONGO_URL

mongo = MongoCli(MONGO_URL)
db = mongo.usersdb

async def get_users():
    return [user['user'] async for user in db.users.find()]

async def add_user(user):
    if not await db.users.find_one({"user": user}):
        await db.users.insert_one({"user": user})

async def del_user(user):
    await db.users.delete_one({"user": user})
