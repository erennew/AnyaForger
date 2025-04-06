from aiohttp import web
from plugins import web_server
import time
import qrcode
import io
import asyncio
from pyrogram.types import Message
START_TIME = time.time()

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode, ChatMemberStatus
import sys
from datetime import datetime

from config import (
    API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS,
    FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2,
    FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4,
    CHANNEL_ID, PORT, JOIN_REQUEST_ENABLE
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="AnyaFileBot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER
        self.join_request_links = {}
        self.qr_login_enabled = False

    async def generate_qr_code(self, session_string: str):
        """Generate QR code for login"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(session_string)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return buf

    async def start(self, use_qr=False, except_ids=None):
        self.LOGGER(__name__).info("🍪 Starting AnyaBot initialization... Waku waku~")
        await super().start()
        self.uptime = datetime.now()

        try:
            usr_bot_me = await self.get_me()
            if usr_bot_me is None:
                raise Exception("get_me() returned None. Invalid BOT_TOKEN?")
            self.username = usr_bot_me.username
        except Exception as e:
            self.LOGGER(__name__).error(f"❌ Mission failed! Couldn't fetch bot info: {e}")
            self.LOGGER(__name__).info("🍪 Check your TG_BOT_TOKEN and ensure Anya isn't blocked!")
            sys.exit()

        # Anya's Secret Clubs (Force Sub Channels with Join Requests)
        force_sub_channels = {
            1: FORCE_SUB_CHANNEL_1,  # 🍪 Peanut Club
            2: FORCE_SUB_CHANNEL_2,  # 🦁 Bond's Den
            3: FORCE_SUB_CHANNEL_3,  # 🎭 Spy Network
            4: FORCE_SUB_CHANNEL_4   # 💖 Assassin Guild
        }

        for idx, channel in force_sub_channels.items():
            if channel:
                try:
                    chat = await self.get_chat(channel)
                    
                    # Create join request link if enabled
                    if JOIN_REQUEST_ENABLE:
                        invite = await self.create_chat_invite_link(
                            chat_id=channel,
                            creates_join_request=True
                        )
                        link = invite.invite_link
                        self.join_request_links[f"join_request_{idx}"] = invite
                        self.LOGGER(__name__).info(f"🔗 Created join request link for channel {idx}")
                    else:
                        link = chat.invite_link or await self.export_chat_invite_link(channel)
                    
                    setattr(self, f"invitelink{'' if idx == 1 else idx}", link)
                    self.LOGGER(__name__).info(f"✅ Secret Club {idx} link secured!")
                    
                except Exception as e:
                    self.LOGGER(__name__).warning(f"🍪 Oh no! Couldn't get channel {idx} link: {e}")
                    self.LOGGER(__name__).warning(f"Check FORCE_SUB_CHANNEL_{idx} and ensure Anya has admin rights!")
                    self.LOGGER(__name__).info("\n🍪 Bot Stopped. Join https://t.me/weebs_support for backup")
                    sys.exit()

        # Secret File Vault (DB Channel Check)
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(
                chat_id=db_channel.id, 
                text="🍪 Anya's File Vault is Online! Waku waku~"
            )
            await test.delete()
            self.LOGGER(__name__).info("🔐 Vault connection established! For world peace!")
        except Exception as e:
            self.LOGGER(__name__).warning(f"🔐 Vault breach! Check CHANNEL_ID and admin rights: {e}")
            self.LOGGER(__name__).info("\n🍪 Bot Stopped. Join https://t.me/weebs_support for backup")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        
        # QR Login Feature
        if use_qr:
            try:
                session_string = await self.export_session_string()
                qr_buffer = await self.generate_qr_code(session_string)
                await self.send_photo(
                    chat_id=except_ids[0] if except_ids else "me",
                    photo=qr_buffer,
                    caption="🔑 Scan this QR to login as AnyaBot! (Expires in 5 mins)"
                )
                self.qr_login_enabled = True
                self.LOGGER(__name__).info("🔑 QR login generated successfully!")
            except Exception as e:
                self.LOGGER(__name__).warning(f"❌ Failed to generate QR login: {e}")

        # Uptime Monitoring
        async def uptime_monitor():
            while True:
                await asyncio.sleep(3600)  # Every hour
                uptime = datetime.now() - self.uptime
                self.LOGGER(__name__).info(f"⏰ AnyaBot uptime: {uptime}")

        asyncio.create_task(uptime_monitor())

        self.LOGGER(__name__).info(f"🍪 AnyaBot Running as @{self.username}\n\n💖 Created for world peace by \nhttps://t.me/CulturedTeluguweeb")
        self.LOGGER(__name__).info(r"""
  　　∧,,,∧
　(；´･ω･) Waku waku!
　 /　　　ﾉ
　し―-Ｊ　 Anya's File Bot
   is now operational!
   For world peace! 💖
""")

        # Enhanced Web Server
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        site = web.TCPSite(app, bind_address, PORT)
        await site.start()
        self.LOGGER(__name__).info(f"🌐 WISE Headquarters active at port {PORT}")

        # Join Request Monitoring
        if JOIN_REQUEST_ENABLE:
            @self.on_chat_join_request()
            async def handle_join_request(client, update):
                try:
                    user = update.from_user
                    chat = update.chat
                    
                    self.LOGGER(__name__).info(f"📨 Join request from {user.id} in {chat.id}")
                    
                    # Add your custom approval logic here
                    # Example: await update.approve()  
                    # Or: await update.decline()
                    
                except Exception as e:
                    self.LOGGER(__name__).error(f"❌ Failed to handle join request: {e}")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("🍪 AnyaBot going to sleep... Heh!")

    async def check_user_status(self, user_id: int, chat_id: int) -> bool:
        """Check if user is subscribed to channel"""
        try:
            member = await self.get_chat_member(chat_id, user_id)
            return member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]
        except Exception as e:
            self.LOGGER(__name__).error(f"❌ Failed to check user status: {e}")
            return False

    async def send_log_message(self, text: str):
        """Send log message to admin"""
        try:
            await self.send_message(chat_id=OWNER_ID, text=text)
        except Exception as e:
            self.LOGGER(__name__).error(f"❌ Failed to send log message: {e}")

__all__ = ["Bot", "START_TIME"]
