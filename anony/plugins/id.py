# Copyright (c) 2025
# Licensed under the MIT License.

from pyrogram import filters
from pyrogram.enums import ParseMode, ChatType, MessageEntityType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from anony import app, lang


@app.on_message(filters.command("id") & ~app.bl_users)
@lang.language()
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    reply = message.reply_to_message
    user = None

    # 🔁 1. Reply check
    if reply and reply.from_user:
        user = reply.from_user

    # 🔁 2. Mention entities (@username or text mention)
    elif message.entities:
        for entity in message.entities:
            if entity.type == MessageEntityType.TEXT_MENTION:
                user = entity.user
                break
            elif entity.type == MessageEntityType.MENTION:
                username = message.text[entity.offset: entity.offset + entity.length]
                try:
                    user = await client.get_users(username)
                    break
                except Exception:
                    continue

    # 🔁 3. Argument like /id @username or /id user_id
    elif len(message.command) >= 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user = await client.get_users(split)
        except Exception:
            return await message.reply_text(
                message.lang.get("id_not_found", "This user doesn't exist."),
                quote=True,
            )

    # 🧾 OUTPUT LOGIC
    if user:
        text = f"<b>{message.lang.get('id_user', 'ᴜsᴇʀ ɪᴅ')}:</b> <code>{user.id}</code>"
        copy_text = str(user.id)
    elif chat.type == ChatType.PRIVATE:
        text = f"<b>{message.lang.get('id_your', 'ʏᴏᴜʀ ɪᴅ')}:</b> <code>{your_id}</code>"
        copy_text = str(your_id)
    else:
        text = f"<b>{message.lang.get('id_chat', 'ᴄʜᴀᴛ ɪᴅ')}:</b> <code>{chat.id}</code>"
        copy_text = str(chat.id)

    # 🧷 Copy button
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(message.lang.get("id_copy", "𝖢𝗈𝗉𝗒"), copy_text=copy_text)]]
    )

    await message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
        reply_markup=keyboard,
        quote=True,
    )
