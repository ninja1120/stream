import asyncio
import random
import time
from sys import version as pyver
from typing import Dict, List, Union

import psutil
from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from Yukki import ASSIDS, BOT_ID, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Yukki import boottime as bot_start_time
from Yukki import db, random_assistant
from Yukki.Core.PyTgCalls import Yukki
from Yukki.Database import (add_nonadmin_chat, add_served_chat,
                            blacklisted_chats, get_assistant, get_authuser,
                            get_authuser_names, get_start, is_nonadmin_chat,
                            is_served_chat, remove_active_chat,
                            remove_nonadmin_chat, save_assistant, save_start)
from Yukki.Decorators.admins import ActualAdminCB
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (custommarkup, dashmarkup, setting_markup,
                          setting_markup2, start_pannel, usermarkup, volmarkup)
from Yukki.Utilities.assistant import get_assistant_details
from Yukki.Utilities.ping import get_readable_time

welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id == BOT_ID:
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        f"تم وضع مجموعة الدردشة الخاصة بك [{message.chat.title}] في القائمة السوداء! \ n \ n اطلب من أي مستخدم Sudo إضافة الدردشة إلى القائمة البيضاء"
                    )
                    return await app.leave_chat(chat_id)
                _assistant = await get_assistant(message.chat.id, "assistant")
                if not _assistant:
                    ran_ass = random.choice(random_assistant)
                    assis = {
                        "saveassistant": ran_ass,
                    }
                    await save_assistant(message.chat.id, "assistant", assis)
                else:
                    ran_ass = _assistant["saveassistant"]
                (
                    ASS_ID,
                    ASS_NAME,
                    ASS_USERNAME,
                    ASS_ACC,
                ) = await get_assistant_details(ran_ass)
                out = start_pannel()
                await message.reply_text(
                    f"مرحبًا بك في {MUSIC_BOT_NAME} \ n \ n قدم لي كمسؤول في مجموعتك وإلا فلن أعمل بشكل صحيح. \ n \ n اسم المستخدم المساعد: - @ {ASS_USERNAME} \ n معرف المساعد: - {ASS_ID}",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                )
            if member.id in ASSIDS:
                return await remove_active_chat(chat_id)
            if member.id in OWNER_ID:
                return await message.reply_text(
                    f"انضم مالك {MUSIC_BOT_NAME} [{member.mention}] للتو إلى محادثتك."
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"انضم عضو من مستخدم {MUSIC_BOT_NAME} [{member.mention}] إلى محادثتك."
                )
            return
        except:
            return


@app.on_message(filters.command(["help", "start"]) & filters.group)
@PermissionCheck
async def useradd(_, message: Message):
    out = start_pannel()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"شكرًا لاستضافتي في {message.chat.title}. \ n {MUSIC_BOT_NAME} حي. \ n \ n للحصول على أي مساعدة أو مساعدة ، تحقق من مجموعة الدعم وقناتنا.",
            reply_markup=InlineKeyboardMarkup(out[1]),
        ),
    )


@app.on_message(filters.command("settings") & filters.group)
@PermissionCheck
async def settings(_, message: Message):
    c_id = message.chat.id
    _check = await get_start(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_start(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    text, buttons = setting_markup2()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"{text} \ n \ n ** المجموعة: ** {message.chat.title} \ n ** معرف المجموعة: ** {message.chat.id} \ n ** مستوى الصوت: ** {volume}%",
            reply_markup=InlineKeyboardMarkup(buttons),
        ),
    )


@app.on_callback_query(filters.regex("okaybhai"))
async def okaybhai(_, CallbackQuery):
    await CallbackQuery.answer("Going Back ...")
    out = start_pannel()
    await CallbackQuery.edit_message_text(
        text=f"شكرًا لاستضافتي في {CallbackQuery.message.chat.title}. \ n {MUSIC_BOT_NAME} على قيد الحياة. \ n \ n للحصول على أي مساعدة أو مساعدة ، تحقق من مجموعة الدعم والقناة.",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("Bot Settings ...")
    text, buttons = setting_markup()
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_start(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_start(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("EVE"))
@ActualAdminCB
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("Changes Saved")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n وضع أوامر المشرف إلى ** الجميع ** \ n \ n الآن يمكن لأي شخص موجود في هذه المجموعة تخطي الموسيقى وإيقافها مؤقتًا واستئنافها وإيقافها. \ n \ n تم التغييرات بواسطة @ {check}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "تم بالفعل تعيين وضع الأوامر على الجميع", show_alert=True
        )


@app.on_callback_query(filters.regex("AMS"))
@ActualAdminCB
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "تم بالفعل تعيين وضع الأوامر على ADMINS فقط", show_alert=True
        )
    else:
        await CallbackQuery.answer("Changes Saved")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n تعيين وضع الأوامر على ** المشرفون ** \ n \ n الآن يمكن للمشرفين الموجودين في هذه المجموعة فقط تخطي الموسيقى وإيقافها مؤقتًا واستئنافها وإيقافها. \ n \ n تم إجراء التغييرات بواسطة @ {check}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("بالفعل في أفضل جودة", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("Bot Settings ...")
        text, buttons = volmarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("Bot Settings ...")
        text, buttons = usermarkup()
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "المشرفون فقط"
        else:
            current = "Everyone"
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n \ n حاليًا من يمكنه استخدام {MUSIC_BOT_NAME}: - ** {current} ** \ n \ n ** ⁉️ ما هذا؟ ** \ n \ n ** 👥 الجميع: - ** يمكن لأي شخص استخدام أوامر {MUSIC_BOT_NAME} (تخطي ، إيقاف مؤقت ، استئناف ، إلخ) الموجودة في هذه المجموعة. \ n \ n ** 🙍 المسؤول فقط: - ** المسؤولون والمفوضون فقط يمكن للمستخدمين استخدام جميع أوامر {MUSIC_BOT_NAME}.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("Dashboard...")
        text, buttons = dashmarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n \ n تحقق من {MUSIC_BOT_NAME} إحصائيات النظام في لوحة القيادة هنا! سيتم إضافة المزيد من الوظائف قريبًا جدًا! استمر في التحقق من قناة الدعم.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("Bot Settings ...")
        text, buttons = custommarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة ...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة ...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة ...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("Nلا توجد مكالمة جماعية نشطة ...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة ...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة ....")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("لا توجد مكالمة جماعية نشطة ...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text} \ n \ n ** المجموعة: ** {c_title} \ n ** معرف المجموعة: ** {c_id} \ n ** مستوى الصوت: ** {volume}٪ \ n ** جودة الصوت: ** أفضل الافتراضي",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("Auth Users!")
        text, buttons = usermarkup()
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text} \ n \ n لم يتم العثور على مستخدمين معتمدين \ n \ n يمكنك السماح لأي شخص غير مسؤول باستخدام أوامر المسؤول الخاصة بي عن طريق / المصادقة والحذف باستخدام / unauth",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "إحضار المستخدمين المصرح لهم ... الرجاء الانتظار"
            )
            msg = f"**Authorised Users List[AUL]:**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
                user_id = _note["auth_user_id"]
                user_name = _note["auth_name"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"    ┗ Added By:- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"Bot's Uptime: {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"Bot's Cpu Usage: {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"Bot's Memory Usage: {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"Yukki Disk Usage: {diske}%", show_alert=True
        )
