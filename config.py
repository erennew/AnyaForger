# (©) WeekendsBotz - Anya Forger Edition 🍪
import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

# ========== ANYA'S SECRET MISSION CONFIG ========== #
# 🍪 Waku waku! Anya's bot configuration for world peace! 💖

# Bot token from @Botfather (Anya's secret code)
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7988129609:AAHIJGSZm2-Ryso22AR4X5s05ZF-HaMmfuc")

# API credentials from my.telegram.org (For WISE operations)
APP_ID = int(os.environ.get("APP_ID", "24500584"))
API_HASH = os.environ.get("API_HASH", "449da69cf4081dc2cc74eea828d0c490")

# Channel IDs (Anya's secret storage locations)
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002448203068"))  # Main files channel
FORCE_SUB_CHANNEL_1 = int(os.environ.get("FORCE_SUB_CHANNEL_1", "-1002650862527"))  # 🍪 Peanut Club
FORCE_SUB_CHANNEL_2 = int(os.environ.get("FORCE_SUB_CHANNEL_2", "-1002331321194"))  # 🦁 Bond's Den
FORCE_SUB_CHANNEL_3 = int(os.environ.get("FORCE_SUB_CHANNEL_3", "-1001956677010"))  # 🎭 Spy Network
FORCE_SUB_CHANNEL_4 = int(os.environ.get("FORCE_SUB_CHANNEL_4", "-1002508438247"))  # 💖 Assassin Guild

# Mission Control (Loid is owner)
OWNER_ID = int(os.environ.get("OWNER_ID", "1047253913"))

# Port for web server (WISE headquarters)
PORT = os.environ.get("PORT", "8080")

# Database (Anya's secret peanut storage)
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://chattaravikiran2001:6nJQC6pb3wLf1zCu@cluster1.daxfzgr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster1")

# Join Request Feature (Secret handshake)
JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", None)

# Worker clones (Anya's helpers)
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# ========== ANYA'S MESSAGES ========== #
# Start Message (Anya's introduction)
START_PIC = os.environ.get("START_PIC","")
START_MSG = os.environ.get(
    "START_MESSAGE", 
    "🍪 Waku waku {mention}!\n\n<blockquote>Anya can store anime/movie files in @CulturedTeluguweeb channel!\nOther users can access them with special links. For world peace!</blockquote>"
)

# Force Subscribe Message (Anya's requirements)
FORCE_PIC = os.environ.get("FORCE_PIC", "")
FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE", 
    "🍪 Ara ara!! {mention}\n\n<b><blockquote>You're missing out on serious spy action!\n"
    "To unlock all features and access files, join all of Anya's secret clubs below!</blockquote></b>"
)

# Custom Caption (Anya's notes)
CUSTOM_CAPTION = os.environ.get("@Ongoing_Weekends")

# Pictures Collection (Anya's favorite images)
PICS = (os.environ.get("PICS", "https://envs.sh/sJX.jpg https://envs.sh/Uc0.jpg https://envs.sh/UkA.jpg https://envs.sh/Uk_.jpg https://envs.sh/Ukc.jpg https://envs.sh/UkZ.jpg https://envs.sh/UkK.jpg")).split()

# Security Settings (Top secret!)
PROTECT_CONTENT = False if os.environ.get('PROTECT_CONTENT', "True") == "True" else False
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'False'

# ========== AUTO DELETE SETTINGS ========== #
# Self-destruct protocol (For mission security)
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "900"))  # 15 minutes

# Convert to human-readable format
minutes = AUTO_DELETE_TIME // 60
seconds = AUTO_DELETE_TIME % 60
AUTO_DELETE_HUMAN = f"{minutes} minute{'s' if minutes != 1 else ''} {seconds} second{'s' if seconds != 1 else ''}"

# Auto-delete messages
AUTO_DELETE_MSG = os.environ.get(
    "AUTO_DELETE_MSG",
    f"⚠️ Mission alert!\n\n<blockquote>This file will self-destruct in {AUTO_DELETE_HUMAN}.\n"
    f"Save important content before time runs out! Waku waku~</blockquote>"
)

AUTO_DEL_SUCCESS_MSG = os.environ.get(
    "AUTO_DEL_SUCCESS_MSG",
    "<blockquote>🍪 Mission complete! File destroyed successfully. Heh!</blockquote>"
)

# ========== ADMIN TEAM ========== #
# WISE Agents (Approved by Loid)
try:
    ADMINS = [int(x) for x in (os.environ.get("ADMINS", "5826613686 5548954124 7378365553 6465096751 1309776707 7186887048").split())]
except ValueError:
    raise Exception("Anya found invalid agents in ADMINS list!")

ADMINS.extend([OWNER_ID, 6266529037])  # Loid and backup admin

# ========== LOGGING ========== #
# Anya's mission log
LOG_FILE_NAME = "anya_mission_log.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

# Reduce Pyrogram noise
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

# ========== SPECIAL MESSAGES ========== #
BOT_STATS_TEXT = "<b><blockquote>🍪 ANYA'S STATUS REPORT</b>\n{uptime}\n\nCurrent mission: File sharing for world peace!</blockquote>"
USER_REPLY_TEXT = "<blockquote>🍪 Waku waku! I only work for my kawaii @CulturedTeluguweeb! For world peace!</blockquote>"
