# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters

from database.filterdb import (
    add_filters,
    all_filters,
    del_filters,
    filters_del,
    filters_info,
)
import re
from main_start.config_var import Config
from main_start.core.decorators import speedo_on_cmd, listen
from main_start.helper_func.basic_helpers import edit_or_reply, get_text


@speedo_on_cmd(
    ["delfilter"],
    cmd_help={"help": "Delete A Filter!", "example": "{ch}delfilter (filter name)"},
    group_only=True
)
async def del_filterz(client, message):
    engine = message.Engine
    note_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    note_name = get_text(message)
    if not note_name:
        await note_.edit(engine.get_string("INPUT_REQ").format("Keyword"))
        return
    note_name = note_name.lower()
    if not await filters_info(note_name, int(message.chat.id)):
        await note_.edit(engine.get_string("FILTER_1").format("FILTERS", note_name))
        return
    await del_filters(note_name, int(message.chat.id))
    await note_.edit(engine.get_string("FILTER_2").format("Filter", note_name))


@speedo_on_cmd(
    ["filters"],
    cmd_help={"help": "List All The Filters In The Chat!", "example": "{ch}filters"},
    group_only=True
)
async def show_filters(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    poppy = await all_filters(int(message.chat.id))
    if poppy is False:
        await pablo.edit(engine.get_string("FILTER_3").format("Filters"))
        return
    kk = "".join(f"\n > `{Escobar.get('keyword')}`" for Escobar in poppy)
    mag = engine.get_string("LIST_OF").format("Filters", message.chat.title, kk)
    await pablo.edit(mag)


@speedo_on_cmd(
    ["savefilter"],
    cmd_help={
        "help": "Save A Filter!",
        "example": "{ch}savefilter (filter name) (replying to message)",
    },
    group_only=True
)
async def s_filters(client, message):
    engine = message.Engine
    note_ = await edit_or_reply(message, engine.get_string("PROCESSING"))
    note_name = get_text(message)
    if not note_name:
        await note_.edit(engine.get_string("INPUT_REQ").format("KeyWord"))
        return
    if not message.reply_to_message:
        await note_.edit(engine.get_string("REPLY_MSG"))
        return
    note_name = note_name.lower()
    msg = message.reply_to_message
    copied_msg = await msg.copy(int(Config.LOG_GRP))
    await add_filters(note_name, int(message.chat.id), copied_msg.message_id)
    await note_.edit(engine.get_string("FILTER_5").format(note_name, "Filters"))


@listen(filters.incoming & ~filters.edited & filters.group & ~filters.private & ~filters.me)
async def reply_filter_(client, message):
    if not message:
        return
    owo = message.text or message.caption
    is_m = False
    if not owo:
        return
    al_fil = await all_filters(int(message.chat.id))
    if not al_fil:
        return
    al_fill = [all_fil.get("keyword") for all_fil in al_fil]
    owo = owo.lower()
    for filter_s in al_fill:
        pattern = r"( |^|[^\w])" + re.escape(filter_s) + r"( |$|[^\w])"
        if re.search(pattern, owo, flags=re.IGNORECASE):
            f_info = await filters_info(filter_s, int(message.chat.id))
            m_s = await client.get_messages(int(Config.LOG_GRP), f_info["msg_id"])
            if await is_media(m_s):
                text_ = m_s.caption or ""
                is_m = True
            else:
                text_ = m_s.text or ""
            if text_ != "":
                mention = message.from_user.mention
                user_id = message.from_user.id
                user_name = message.from_user.username or "No Username"
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name or "No Last Name"
                text_ = text_.format(mention=mention, user_id=user_id, user_name=user_name, first_name=first_name, last_name=last_name)
            if not is_m:
                await client.send_message(
                message.chat.id,
                text_,
                reply_to_message_id=message.message_id)
            else:
                await m_s.copy(
                chat_id=int(message.chat.id),
                caption=text_,
                reply_to_message_id=message.message_id,
        )

async def is_media(message):
    return bool(
        (
            message.photo
            or message.video
            or message.document
            or message.audio
            or message.sticker
            or message.animation
            or message.voice
            or message.video_note
        )
    )

@speedo_on_cmd(
    ["delfilters"],
    cmd_help={"help": "Delete All The Filters in chat!", "example": "{ch}delfilters"},
)
async def del_all_filters(client, message):
    engine = message.Engine
    pablo = await edit_or_reply(message, engine.get_string("PROCESSING"))
    poppy = await all_filters(int(message.chat.id))
    if poppy is False:
        await pablo.edit(engine.get_string("FILTER_3").format("Filters"))
        return
    await filters_del(int(message.chat.id))
    await pablo.edit(engine.get_string("REMOVED_ALL").format("Filters"))
