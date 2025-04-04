#(©) WeekendsBotz

import base64
import re
import asyncio
import logging 
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4, ADMINS, AUTO_DELETE_TIME, AUTO_DEL_SUCCESS_MSG
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait

async def is_subscribed(filter, client, update):
    if not any([FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4]):
        return True

    user_id = update.from_user.id

    if user_id in ADMINS:
        return True

    for channel_id in [FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4]:
        if not channel_id:
            continue

        try:
            member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER):
                return False
        except UserNotParticipant:
            return False
        except Exception as e:
            logging.warning(f"Error checking membership in channel {channel_id}: {e}")
            return False

    return True

async def encode(string):
    base64_bytes = base64.urlsafe_b64encode(string.encode("ascii"))
    return base64_bytes.decode("ascii").rstrip("=")

async def decode(base64_string):
    padded = base64_string + "=" * (-len(base64_string) % 4)
    string_bytes = base64.urlsafe_b64decode(padded.encode("ascii"))
    return string_bytes.decode("ascii")

async def get_messages(client, message_ids):
    messages = []
    total = 0
    while total < len(message_ids):
        chunk = message_ids[total:total + 200]
        try:
            msgs = await client.get_messages(chat_id=client.db_channel.id, message_ids=chunk)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(chat_id=client.db_channel.id, message_ids=chunk)
        except Exception as e:
            logging.warning(f"Failed fetching messages chunk: {e}")
            msgs = []
        messages.extend(msgs)
        total += len(chunk)
    return messages

async def get_message_id(client, message):
    if message.forward_from_chat and message.forward_from_chat.id == client.db_channel.id:
        return message.forward_from_message_id
    elif message.forward_sender_name:
        return 0
    elif message.text:
        match = re.match(r"https://t.me/(?:c/)?(.*)/(\d+)", message.text)
        if match:
            channel_id, msg_id = match.group(1), int(match.group(2))
            if channel_id.isdigit() and f"-100{channel_id}" == str(client.db_channel.id):
                return msg_id
            elif channel_id == client.db_channel.username:
                return msg_id
    return 0

def get_readable_time(seconds: int) -> str:
    count = 0
    time_list = []
    suffixes = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        seconds, val = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if val == 0 and seconds == 0:
            break
        time_list.append(f"{int(val)}{suffixes[count - 1]}")
    return ", ".join(reversed(time_list)) if len(time_list) == 4 else ":".join(reversed(time_list))

async def delete_file(messages, client, process):
    await asyncio.sleep(AUTO_DELETE_TIME)
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            logging.error(f"Failed to delete message {msg.id}: {e}")

    try:
        await process.edit_text(AUTO_DEL_SUCCESS_MSG)
    except Exception as e:
        logging.warning(f"Failed to edit process message: {e}")

subscribed = filters.create(is_subscribed)
