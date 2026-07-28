from os import getenv

# Required
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
SESSION_STRING = getenv("SESSION_STRING")
MONGO_URL = getenv("MONGO_URL")
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-100123456789"))

# Optional
OWNER_ID = int(getenv("OWNER_ID", "0"))
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "0").split()))
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "300"))
START_IMG_URL = getenv("START_IMG_URL", "https://graph.org/file/5d73d3a4940ea78fbc7f3.jpg")
