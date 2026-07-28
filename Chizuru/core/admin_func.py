from config import SUDO_USERS
from typing import List, Dict, Callable

admins: Dict[int, List[int]] = {}

def set_admins(chat_id: int, admins_: List[int]):
    admins[chat_id] = admins_

def get_admins(chat_id: int):
    return admins.get(chat_id, [])

def authorized_users(func: Callable) -> Callable:
    async def decorator(client, message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)
        admins_list = get_admins(message.chat.id)
        if message.from_user.id in admins_list:
            return await func(client, message)
    return decorator
