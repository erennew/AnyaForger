from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
from config import (
    API_HASH,
    APP_ID,
    LOGGER,
    TG_BOT_TOKEN,
    TG_BOT_WORKERS,
    FORCE_SUB_CHANNEL_1,
    FORCE_SUB_CHANNEL_2,
    FORCE_SUB_CHANNEL_3,
    FORCE_SUB_CHANNEL_4,
    CHANNEL_IDS,
    PORT
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_BOT_TOKEN,
            workers=TG_BOT_WORKERS,
            plugins={"root": "plugins"}
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Force Subscription Channels - OLD STYLE
        if FORCE_SUB_CHANNEL_1:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL_1)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL_1)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL_1)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from FORCE_SUB_CHANNEL_1!")
                self.LOGGER(__name__).info("Bot Stopped. Join https://t.me/weebs_support for support")
                sys.exit()

        if FORCE_SUB_CHANNEL_2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL_2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL_2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL_2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from FORCE_SUB_CHANNEL_2!")
                self.LOGGER(__name__).info("Bot Stopped. Join https://t.me/weebs_support for support")
                sys.exit()

        if FORCE_SUB_CHANNEL_3:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL_3)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL_3)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL_3)).invite_link
                self.invitelink3 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from FORCE_SUB_CHANNEL_3!")
                self.LOGGER(__name__).info("Bot Stopped. Join https://t.me/weebs_support for support")
                sys.exit()

        if FORCE_SUB_CHANNEL_4:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL_4)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL_4)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL_4)).invite_link
                self.invitelink4 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from FORCE_SUB_CHANNEL_4!")
                self.LOGGER(__name__).info("Bot Stopped. Join https://t.me/weebs_support for support")
                sys.exit()

        # DB Channel Test
        try:
            db_channel = await self.get_chat(CHANNEL_IDS[0])
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="✅ Bot is Online!")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make sure the bot is admin in DB channel. CHANNEL_IDS: {CHANNEL_IDS}")
            self.LOGGER(__name__).info("Bot Stopped. Join https://t.me/weebs_support for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)

        self.username = usr_bot_me.username
        self.LOGGER(__name__).info(f"Bot Running as @{self.username}")
        self.LOGGER(__name__).info(f"Created by https://t.me/CulturedTeluguweeb")

        # Fancy ASCII Banner
        self.LOGGER(__name__).info(r"""
  ┈┈┈╱▔▔▔▔▔▔╲┈╭━━━━━━━╮┈┈
┈┈▕┈╭━╮╭━╮┈▏┃ℝ𝕒𝕧𝕚 𝔹𝕠𝕥
┈┈▕┈┃╭╯╰╮┃┈▏╰┳━━━━━━╯┈┈
┈┈▕┈╰╯╭╮╰╯┈▏┈┃┈┈┈┈┈
┈┈▕┈┈┈┃┃┈┈┈▏━╯┈┈┈┈┈
┈┈▕┈┈┈╰╯┈┈┈▏┈┈┈┈┈┈┈
┈┈▕╱╲╱╲╱╲╱╲▏┈┈┈┈┈┈┈
""")


        # Start web server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
