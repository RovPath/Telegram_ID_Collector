from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from utils.texts import TEXTS
from database.manager import DBManager

router = Router()


def get_lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 RU", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇺🇸 EN", callback_data="lang:en"),
            ]
        ]
    )


@router.message(CommandStart())
async def cmd_start(message: Message, lang: str):
    await message.answer(TEXTS[lang]["start"], reply_markup=get_lang_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def select_lang(callback: CallbackQuery, db: DBManager):
    new_lang = callback.data.split(":")[1]
    await db.set_lang(callback.from_user.id, new_lang)
    await callback.message.edit_text(TEXTS[new_lang]["set"])
    await callback.answer()


@router.message(Command("help"))
async def help_command(message: Message, lang: str):
    await message.answer(text=TEXTS[lang]["help"])


@router.message(Command("myid"))
async def myid_command(message: Message, lang: str):
    t = TEXTS[lang]
    username = f"@{message.from_user.username}" if message.from_user.username else "❌ N/A"
    last_name = message.from_user.last_name if message.from_user.last_name else "❌ N/A"
    text = (
        f"{t['myid_title']}\n"
        "┌──────────────────\n"
        f"│ 👤 <b>{t['personal_id']}:</b> <code>{message.from_user.id}</code>\n"
        f"│ 👥 <b>{t['username']}:</b> {username}\n"
        f"│ 📝 <b>{t['first_name']}:</b> {message.from_user.first_name}\n"
        f"│ 📝 <b>{t['last_name']}:</b> {last_name}\n"
        f"│ 💬 <b>{t['chat_id']}:</b> <code>{message.chat.id}</code>\n"
        f"│ 🏷️ <b>{t['chat_type']}:</b> {message.chat.type}\n"
        f"│ ✉️ <b>{t['message_id']}:</b> <code>{message.message_id}</code>\n"
        "└──────────────────"
    )
    await message.answer(text=text)


@router.message(Command("chatid"))
async def chatid_command(message: Message, lang: str):
    t = TEXTS[lang]
    chat = message.chat
    chat_title = "❌ N/A"
    if chat.type == "private":
        chat_title = f"{chat.first_name or ''} {chat.last_name or ''}".strip()
    elif hasattr(chat, "title") and chat.title:
        chat_title = chat.title
    chat_username = "❌ N/A"
    if hasattr(chat, "username") and chat.username:
        chat_username = f"@{chat.username}"
    text = (
        f"{t['chatid_title']}\n"
        "┌──────────────────\n"
        f"│ 💬 <b>{t['chat_id']}:</b> <code>{chat.id}</code>\n"
        f"│ 🏷️ <b>{t['chat_type']}:</b> {chat.type}\n"
        f"│ 📝 <b>{t['title']}:</b> {chat_title}\n"
        f"│ 👤 <b>{t['username']}:</b> {chat_username}\n"
        f"│ ✉️ <b>{t['message_id']}:</b> <code>{message.message_id}</code>\n"
        "└──────────────────"
    )
    await message.answer(text=text)


@router.message(Command("id"))
async def id_info_reply(message: Message, lang: str):
    t = TEXTS[lang]
    if not message.reply_to_message:
        return await message.answer(t["id_reply_required"])
    reply = message.reply_to_message
    date_str = reply.date.strftime("%Y-%m-%d %H:%M:%S") if reply.date else "N/A"
    lines = [
        f"┌──────────────────",
        f"│ 📋 <b>{t['id_title']}</b>",
        f"│ 🆔 <b>{t['message_id']}:</b> <code>{reply.message_id}</code>",
        f"│ 📅 <b>{t['id_date']}:</b> {date_str}",
    ]
    if reply.from_user:
        lines.append(f"│ 👤 <b>{t['id_from']}:</b> {reply.from_user.full_name} [<code>{reply.from_user.id}</code>]")
    if reply.chat:
        lines.append(f"│ 💬 <b>{t['id_chat']}:</b> <code>{reply.chat.id}</code>")
    lines.append(f"│ 🧩 <b>{t['type']}:</b> {reply.content_type}")
    if reply.text:
        lines.append(f"│ 📄 <b>{t['id_text']}:</b> {reply.text[:200]}")
    if reply.caption:
        lines.append(f"│ 📝 <b>{t['caption']}:</b> {reply.caption[:200]}")
    if reply.photo:
        lines.append(f"│ 🖼️ <b>Photo ID:</b> <code>{reply.photo[-1].file_id}</code>")
    if reply.video:
        lines.append(f"│ 🎥 <b>Video ID:</b> <code>{reply.video.file_id}</code>")
    if reply.document:
        lines.append(f"│ 📄 <b>Document ID:</b> <code>{reply.document.file_id}</code>")
    if reply.audio:
        lines.append(f"│ 🎵 <b>Audio ID:</b> <code>{reply.audio.file_id}</code>")
    if reply.voice:
        lines.append(f"│ 🎤 <b>Voice ID:</b> <code>{reply.voice.file_id}</code>")
    if reply.sticker:
        lines.append(f"│ 🏷️ <b>Sticker ID:</b> <code>{reply.sticker.file_id}</code>")
    if reply.animation:
        lines.append(f"│ 🎞️ <b>Animation ID:</b> <code>{reply.animation.file_id}</code>")
    if reply.location:
        lines.append(f"│ 📍 <b>{t['coordinates']}:</b> {reply.location.latitude}, {reply.location.longitude}")
    if reply.contact:
        lines.append(f"│ 👤 <b>{t['contact_id']}:</b> {reply.contact.phone_number} ({reply.contact.first_name})")
    lines.append("└──────────────────")
    await message.answer("\n".join(lines))
