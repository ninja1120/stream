from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from config import MUSIC_BOT_NAME, SUPPORT_CHANNEL, SUPPORT_GROUP
from Yukki import BOT_USERNAME


def setting_markup2():
    buttons = [
        [
            InlineKeyboardButton(text="🔈 جوده الصوت", callback_data="AQ"),
            InlineKeyboardButton(text="🎚 مستوى الصوت", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="👥 المستخدمون المعتمدون", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="💻 لوحه التحكم", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="✖️ اغلاق", callback_data="close"),
        ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} اعدادات**", buttons


def start_pannel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 قائمة أوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 اعدادات", callback_data="settingm"
                )
            ],
        ]
        return f"🎛  **هذا هو {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 قائمة أوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 اعدادات", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨جروب الدعم", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎛  **هذا هو {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 قائمة أوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 اعدادات", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨القناه الرسمية", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
        ]
        return f"🎛  **هذا هو {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 قائمة أوامر المساعد", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 اعدادات", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨القناه الرسمية", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="📨جروب الدعم", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎛  **هذا هو {MUSIC_BOT_NAME}**", buttons


def private_panel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 قائمة أوامر المساعد",
                    callback_data="search_helper_mess",
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ اضفني الى مجموعتك",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
        ]
        return f"🎛  **This is {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 قائمة أوامر المساعد",
                    callback_data="search_helper_mess",
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ اضفني الى مجموعتك",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨جروب الدعم", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎛  **هذا هو {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 قائمة أوامر المساعد",
                    callback_data="search_helper_mess",
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ اضفني الي مجموعتك",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨القناه الرسمية", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
        ]
        return f"🎛  **هذا هو {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 قائمة أوامر المساعد",
                    callback_data="search_helper_mess",
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ اضفني الى مجموعتك",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨القناه الرسمية", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="📨جروب الدعم ", url=f"{SUPPORT_GROUP}"
                ),
            ],
        ]
        return f"🎛  **هذا هو {MUSIC_BOT_NAME}**", buttons


def setting_markup():
    buttons = [
        [
            InlineKeyboardButton(text="🔈 جودة الصوت", callback_data="AQ"),
            InlineKeyboardButton(text="🎚 مستوى الصوت", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="👥 المستخدمون المعتمدون", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="💻 لوحة التحكم", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="✖️ اغلاق", callback_data="close"),
            InlineKeyboardButton(text="🔙 رجوع", callback_data="okaybhai"),
        ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} اعدادات**", buttons


def volmarkup():
    buttons = [
        [
            InlineKeyboardButton(
                text="🔄 اعادة مستوى الصوت 🔄", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🔈 صوت منخفض ", callback_data="LV"),
            InlineKeyboardButton(text="🔉 صوت متوسط ", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🔊 صوت عالي", callback_data="HV"),
            InlineKeyboardButton(text="🔈 تضخيم الصوت", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 مستوى الصوت 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="🔙 رجوع", callback_data="settingm")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} اعدادات**", buttons


def custommarkup():
    buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼مستوي الصوت  🔼", callback_data="AV")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} اعدادات**", buttons


def usermarkup():
    buttons = [
        [
            InlineKeyboardButton(text="👥 الجميع", callback_data="EVE"),
            InlineKeyboardButton(text="🙍 الادمن", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="📋 قوائم المستخدمين المعتمدين", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="🔙 رجوع", callback_data="settingm")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} إعدادات**", buttons


def dashmarkup():
    buttons = [
        [
            InlineKeyboardButton(text="✔️ مدة التشغيل", callback_data="UPT"),
            InlineKeyboardButton(text="💾 الرامات", callback_data="RAT"),
        ],
        [
            InlineKeyboardButton(text="💻 المعالج", callback_data="CPT"),
            InlineKeyboardButton(text="💽 المساحه", callback_data="DIT"),
        ],
        [InlineKeyboardButton(text="🔙 رجوع", callback_data="settingm")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} Settings**", buttons
