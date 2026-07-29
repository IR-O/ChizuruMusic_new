import os

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

SUDO_USERS = list(
    map(
        int,
        filter(None, os.getenv("SUDO_USERS", "").split())
    )
)

MONGO_URL = os.getenv("MONGO_URL", "")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# Optional Settings
LOG_GROUP_ID = int(os.getenv("LOG_GROUP_ID", "0"))
AUTO_LEAVING_ASSISTANT = (
    os.getenv("AUTO_LEAVING_ASSISTANT", "True").lower() == "true"
)

# Validation
REQUIRED_VARS = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "OWNER_ID": OWNER_ID,
    "MONGO_URL": MONGO_URL,
    "SESSION_STRING": SESSION_STRING,
}

missing = [key for key, value in REQUIRED_VARS.items() if not value]

if missing:
    raise ValueError(
        f"Missing required environment variables: {', '.join(missing)}"
    )
