import os
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
PICS = (os.environ.get("PICS", "https://envs.sh/sJX.jpg https://envs.sh/Uc0.jpg https://envs.sh/UkA.jpg https://envs.sh/Uk_.jpg https://envs.sh/Ukc.jpg https://envs.sh/UkZ.jpg https://envs.sh/UkK.jpg")).split()
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, START_PIC, FORCE_PIC, AUTO_DELETE_TIME, AUTO_DELETE_MSG, JOIN_REQUEST_ENABLE, FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4
from helper_func import subscribed, decode, get_messages, delete_file
from database.database import add_user, del_user, full_userbase, present_user

# Anya-themed messages
ANYA_WAIT = [
    "🍪 Anya is getting your files... waku waku!",
    "🦁 Bond is sniffing out your request...",
    "👀 Reading your mind to find files...",
    "🤫 Secret mission in progress..."
]

ANYA_ERROR = "😵‍💫 Mission failed! Anya couldn't find them..."

async def create_invite_links(client: Client):
    """Create join request links for all force sub channels"""
    links = {}
    channels = {
        1: FORCE_SUB_CHANNEL_1,
        2: FORCE_SUB_CHANNEL_2,
        3: FORCE_SUB_CHANNEL_3,
        4: FORCE_SUB_CHANNEL_4
    }
    
    for num, channel in channels.items():
        if channel:
            try:
                invite = await client.create_chat_invite_link(
                    chat_id=channel,
                    creates_join_request=JOIN_REQUEST_ENABLE
                )
                links[f"invitelink{'' if num == 1 else num}"] = invite.invite_link
                links[f"join_request_{num}"] = invite if JOIN_REQUEST_ENABLE else None
            except Exception as e:
                print(f"Error creating invite link for channel {num}: {e}")
                raise
    return links

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception as e:
            print(f"Error adding user: {e}")

    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
            string = await decode(base64_string)
            argument = string.split("-")
            
            if len(argument) == 3:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            elif len(argument) == 2:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            else:
                return
                
            temp_msg = await message.reply(f"<blockquote>{random.choice(ANYA_WAIT)}</blockquote>")
            messages = await get_messages(client, ids)
            await temp_msg.delete()
            
            track_msgs = []
            for msg in messages:
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name
                ) if bool(CUSTOM_CAPTION) and msg.document else (msg.caption.html if msg.caption else "")
                
                reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None
                
                try:
                    if AUTO_DELETE_TIME > 0:
                        copied_msg = await msg.copy(
                            chat_id=message.from_user.id,
                            caption=caption,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup,
                            protect_content=PROTECT_CONTENT
                        )
                        track_msgs.append(copied_msg)
                    else:
                        await msg.copy(
                            chat_id=message.from_user.id,
                            caption=caption,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup,
                            protect_content=PROTECT_CONTENT
                        )
                        await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    if AUTO_DELETE_TIME > 0:
                        copied_msg = await msg.copy(
                            chat_id=message.from_user.id,
                            caption=caption,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup,
                            protect_content=PROTECT_CONTENT
                        )
                        track_msgs.append(copied_msg)
                    else:
                        await msg.copy(
                            chat_id=message.from_user.id,
                            caption=caption,
                            parse_mode=ParseMode.HTML,
                            reply_markup=reply_markup,
                            protect_content=PROTECT_CONTENT
                        )
                except Exception as e:
                    print(f"Error sending file: {e}")
                    await message.reply_text(f"<blockquote>{ANYA_ERROR}</blockquote>")
                    return

            if track_msgs:
                delete_data = await client.send_message(
                    chat_id=message.from_user.id,
                    text=AUTO_DELETE_MSG.format(time=AUTO_DELETE_TIME)
                )
                asyncio.create_task(delete_file(track_msgs, client, delete_data))
                
        except Exception as e:
            print(f"Error in start command: {e}")
            await message.reply_text(f"<blockquote>{ANYA_ERROR}</blockquote>")
    else:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🍪 About Anya", callback_data="about"),
             InlineKeyboardButton("🦁 Close", callback_data="close")]
        ])
        
        if START_PIC:
            await message.reply_photo(
                photo=random.choice(PICS),
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                quote=True
            )
        else:
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                link_preview_options=True,
                quote=True
            )

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    try:
        links = await create_invite_links(client)
    except Exception as e:
        await message.reply_text("🍪 Anya can't create invite links right now. Try again later!")
        print(f"Error creating invite links: {e}")
        return

    buttons = [
        [
            InlineKeyboardButton("🗄️ Main Vault", url=links.get("invitelink", "#")),
            InlineKeyboardButton("⚙️ Ongoing Machines", url=links.get("invitelink2", "#"))
        ],
        [
            InlineKeyboardButton("📼 Vintage", url=links.get("invitelink3", "#")),
            InlineKeyboardButton("🎯 Completed Ops", url=links.get("invitelink4", "#"))
        ]
    ]
    
    try:
        buttons.append([
            InlineKeyboardButton(
                "🌟 Click Here After Joining",
                url=f"https://t.me/{client.username}?start={message.command[1]}"
            )
        ])
    except IndexError:
        pass

    if FORCE_PIC:
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
    else:
        await message.reply_text(
            text=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
            link_preview_options=True
        )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await message.reply("🍪 Anya is counting agents...")
    users = await full_userbase()
    await msg.edit(f"👥 {len(users)} agents working for world peace!")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        
        progress = await message.reply("<i>🍼 Anya is delivering messages to all agents...</i>")
        
        stats = {"total": 0, "successful": 0, "blocked": 0, "deleted": 0, "failed": 0}
        
        for user_id in query:
            try:
                await broadcast_msg.copy(user_id)
                stats["successful"] += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(user_id)
                stats["successful"] += 1
            except UserIsBlocked:
                await del_user(user_id)
                stats["blocked"] += 1
            except InputUserDeactivated:
                await del_user(user_id)
                stats["deleted"] += 1
            except Exception as e:
                print(f"Broadcast error for {user_id}: {e}")
                stats["failed"] += 1
            stats["total"] += 1

        status = f"""<b>🌟 Broadcast Complete!</b>

👥 Total: <code>{stats['total']}</code>
✅ Success: <code>{stats['successful']}</code>
🚫 Blocked: <code>{stats['blocked']}</code>
💀 Deleted: <code>{stats['deleted']}</code>
❌ Failed: <code>{stats['failed']}</code>"""

        await progress.edit(status)
    else:
        msg = await message.reply("🍪 Reply to a message to broadcast it!")
        await asyncio.sleep(5)
        await msg.delete()
