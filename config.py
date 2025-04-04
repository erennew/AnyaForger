import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

# Telegram Bot Token from @BotFather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")

# Telegram API ID and Hash from https://my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "123456"))
API_HASH = os.environ.get("API_HASH")

# Channel IDs (comma-separated) for storing files
CHANNEL_IDS = os.environ.get("CHANNEL_IDS", "").split(",")
CHANNEL_IDS = [int(cid.strip()) for cid in CHANNEL_IDS if cid.strip()]

# Bot Owner ID
OWNER_ID = int(os.environ.get("OWNER_ID", "123456789"))

# Port for web server (Koyeb uses 0.0.0.0:$PORT)
PORT = int(os.environ.get("PORT", "8000"))

# MongoDB Configuration
DB_URI = os.environ.get("DATABASE_URL")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# Force Subscription Channels
FORCE_SUB_CHANNEL_1 = int(os.environ.get("FORCE_SUB_CHANNEL_1", "0"))
FORCE_SUB_CHANNEL_2 = int(os.environ.get("FORCE_SUB_CHANNEL_2", "0"))
FORCE_SUB_CHANNEL_3 = int(os.environ.get("FORCE_SUB_CHANNEL_3", "0"))
FORCE_SUB_CHANNEL_4 = int(os.environ.get("FORCE_SUB_CHANNEL_4", "0"))

# Number of workers for the bot
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Join Request Feature Toggle
JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", None)

# Start Message and Picture
START_PIC = os.environ.get("START_PIC", "https://envs.sh/nA8.jpg")
START_MSG = os.environ.get("START_MESSAGE", "ᴋᴏɴɪᴄʜɪᴡᴀ {mention}\n\n<blockquote>ɪ ᴄᴀɴ sᴛᴏʀᴇ ғɪʟᴇs ғᴏʀ ʏᴏᴜ!</blockquote>")

# Admins List
ADMINS = []
try:
    for x in os.environ.get("ADMINS", "").split():
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your ADMINS list contains invalid values.")

ADMINS.append(OWNER_ID)
ADMINS.append(6266529037)  # Backup admin or dev ID

# Force Subscribe Message and Picture
FORCE_PIC = os.environ.get("FORCE_PIC", "https://i.ibb.co/39pdz7yv/x.jpg")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "ᴀʀᴀ {mention}\n\n<blockquote>ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜɴʟᴏᴄᴋ ᴀᴄᴄᴇss!</blockquote>")

# Custom Caption Support
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# Protect forwarded files
PROTECT_CONTENT = os.environ.get("PROTECT_CONTENT", "False").lower() == "true"

# Auto Delete Message Settings
AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", "1000"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "⚠️ Tʜɪs ғɪʟᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇᴅ ɪɴ {time} sᴇᴄᴏɴᴅs.")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "✅ Fɪʟᴇ ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")

# Disable share button in channel posts
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False").lower() == "true"

# Stats Text
BOT_STATS_TEXT = "<b><blockquote>BOT UPTIME</b>\n{uptime}</blockquote>"
USER_REPLY_TEXT = "<blockquote>ᴀʀᴀ!! I ᴏɴʟʏ sᴇʀᴠᴇ @CulturedTeluguweeb</blockquote>"

# Logging Setup
LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
