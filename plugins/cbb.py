#(©) WeekendsBotz

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = (
                "<b><blockquote>🔐 ANYA'S SECRET NETWORK 🔐\n\n"
                " 👑 Owner of Spy : <a href='https://t.me/CulturedTeluguWeebBot'>ʀᴀᴠɪ</a>\n"
                "🏢 WISE Headquarters : <a href='https://t.me/CulturedTeluguweeb'>ᴄᴜʟᴛᴜʀᴇᴅ ᴡᴇᴇʙ</a>\n"
                "📡 Current Mission : <a href='https://t.me/+BiVvkpD5ieIxZTNl'>ᴄᴛᴡ ᴏɴɢᴏɪɴɢ</a>\n"
                "🗣️ Spy Chatter : <a href='https://t.me/+IIgB6RgivTI2NzA1'>ᴄᴜʟᴛᴜʀᴇᴅ ᴡᴇᴇʙꜱ</a>"
                "</blockquote></b>"
            ),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⚡ Cℓσѕє", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
