#(©)Rapid_Bots



import os
import re
import asyncio
import time
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.file_id import FileId
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, FL_CHANNEL, CURL, STREAM, DELETE, VERIFY_MSG, VERIFIED_MSG, SRT_VERIFY
from helper_func import subscribed, encode, decode, get_messages, check_token, get_token, verify_user, check_verification
from database.database import db
import logging
from typing import Any, Optional
from pyrogram.raw.types.messages import Messages

logging.basicConfig(level=logging.INFO)

async def delete_file(message: Message):
    await asyncio.sleep(30)
    await message.delete()

async def parse_file_id(message: "Message") -> Optional[FileId]:
    media = get_media_from_message(message)
    if media:
        return FileId.decode(media.file_id)

async def parse_file_unique_id(message: "Messages") -> Optional[str]:
    media = get_media_from_message(message)
    if media:
        return media.file_unique_id

async def get_file_ids(client: Client, chat_id: int, id: int) -> Optional[FileId]:
    message = await client.get_messages(chat_id, id)
    media = get_media_from_message(message)
    file_unique_id = await parse_file_unique_id(message)
    file_id = await parse_file_id(message)
    setattr(file_id, "file_size", getattr(media, "file_size", 0))
    setattr(file_id, "mime_type", getattr(media, "mime_type", ""))
    setattr(file_id, "file_name", getattr(media, "file_name", ""))
    setattr(file_id, "unique_id", file_unique_id)
    return file_id

def get_media_from_message(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media


def get_hash(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, "file_unique_id", "")[:6]

def get_name(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, 'file_name', "")

def get_media_file_size(m):
    media = get_media_from_message(m)
    return getattr(media, "file_size", 0)

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    await db.add_user(client, message)  
    text = message.text
    is_admin = id in ADMINS
    command_params = " ".join(message.command[1:])
    
    # Log command parameters
    logging.info(f"Command Parameters: {command_params}")

    if command_params:
        if command_params.startswith("verify"):
            parts = command_params.split("-", 2)
            if len(parts) == 3:
                verify_userid, token = parts[1:]
                if str(id) == verify_userid:
                    is_valid = await check_token(id, token)
                    if is_valid:
                        await message.reply_text(text=VERIFIED_MSG)
                        await verify_user(id, token)
                    else:
                        return await message.reply_text(
                            text="<b>Expired or invalid Verification Link 🫣 Click /Start And Verify Again 😊</b>"
                        )
    if SRT_VERIFY == "True":
        else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return
        
    if not is_admin: 
        text = message.text
        is_verified = await check_verification(id)
        
        if not is_verified:
            btn = [[
                InlineKeyboardButton("👨‍💻 Verify", url=await get_token(id, f"https://filestore.rapidbots.workers.dev?start="))
                ],[
                InlineKeyboardButton("🔻 How to open and Verify 🔺", url="https://t.me/TamilSk_Demo/3")
            ]]
            await message.reply_text(
                text = VERIFY_MSG,
                protect_content=False,
                
                reply_markup=InlineKeyboardMarkup(btn)
            )
            return
        
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except Exception as e:
            logging.error(f"Exception occurred while splitting text: {e}")
            return
        
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except Exception as e:
                logging.error(f"Exception occurred while calculating start and end: {e}")
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception as e:
                logging.error(f"Exception occurred while processing IDs: {e}")
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            logging.error(f"Exception occurred while getting messages: {e}")
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        delete_tasks = []

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            elif bool(CUSTOM_CAPTION) & bool(msg.video):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename="Video")
            else:
                caption = "" if not msg.caption else msg.caption.html
                
            if msg.video or msg.document:    
                if STREAM == "True":
                    log_msg = await client.copy_message(
                            chat_id=FL_CHANNEL,
                            from_chat_id=client.db_channel.id,
                            message_id=msg.id,
                        )
                    turl = CURL
                    stream = f"{turl}dl/{get_hash(log_msg)}{str(log_msg.id)}"

                    reply_markup = InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("Fast Download Link (Google)", url=stream)]
                        ]
                    )

                else:
                    reply_markup = None
            else:
                reply_markup = None

            try:
                ss = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT())
                if DELETE == "True":
                  tt = await ss.reply_text(f"<b>𝙄𝙈𝙋𝙊𝙍𝙏𝘼𝙉𝙏  ↦↦↦⃟👉 This Movie File will be deleted in 5 minutes. So Please forward this File Before Download 📥</b>",disable_web_page_preview=True, quote=True)
                  delete_tasks.append(asyncio.create_task(delete_file(ss))) 
                  delete_tasks.append(asyncio.create_task(delete_file(tt)))
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                ss = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = ParseMode.HTML, reply_markup = reply_markup, protect_content=PROTECT_CONTENT())
                if DELETE == "True":
                  tt = await ss.reply_text(f"<b>𝙄𝙈𝙋𝙊𝙍𝙏𝘼𝙉𝙏  ↦↦↦⃟👉 This Movie File will be deleted in 5 minutes. So Please forward this File Before Download 📥</b>",disable_web_page_preview=True, quote=True)
                  delete_tasks.append(asyncio.create_task(delete_file(ss))) 
                  delete_tasks.append(asyncio.create_task(delete_file(tt)))
            except Exception as e:
                # Log exceptions
                logging.error(f"Exception occurred while processing messages: {e}")
                pass
        await asyncio.gather(*delete_tasks)
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return
    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##

    
    
@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                "Join Channel",
                url = client.invitelink),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = '🔄 Try Again 🔄',
                    url = f"https://telegram.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await db.total_users_count()
    await msg.edit(f"{users} users are using this bot")

@Bot.on_message(filters.command('channels') & filters.private)
async def channel_text(client: Bot, message: Message):
    channeltext = f"""<b>
╭────────────────╮
                👤 Cʜᴀɴɴᴇʟ List 👤
╰────────────────╯
╭────────────────
✪ Sᴋ Vᴇʀɪғɪᴇᴅ Cʜᴀɴɴᴇʟ'ꜱ
│
│➩ Tamil Movies/Series
│ https://t.me/+lW8rqXwP8qQ0ODZl
│
│➩ Vijay Tv Serials/Shows
│ https://t.me/+Jk4hcVP8A-43ZjZl
│
│➩ Cook With Comali Season 5
│ https://t.me/+G3yps9kTPE04ZDFl
│
│➩ Top Cooku Dupe Cooku
│ https://t.me/+jfivsh1ShrA0MTE1
╰────────────────
Pᴏᴡᴇʀᴇᴅ Bʏ @Tamilsk_Moviez
</b>
"""
    msg = await client.send_message(chat_id=message.chat.id, text=channeltext)

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, m: Message):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Bʀᴏᴀᴅᴄᴀꜱᴛ Sᴛᴀʀᴛᴇᴅ..!") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await db.delete_user(user['_id'])
        done += 1
        if not done % 20:
           await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ: \nTᴏᴛᴀʟ Uꜱᴇʀ {total_users} \nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ: \nCᴏᴍᴩʟᴇᴛᴇᴅ Iɴ `{completed_in}`.\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}")
           
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400
    except UserIsBlocked:
        return 400
    except PeerIdInvalid:
        return 400
    except Exception as e:
        return 500
 
