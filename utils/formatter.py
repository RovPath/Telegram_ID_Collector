from typing import Any, Dict, Optional
from aiogram.types import Message
from utils.texts import TEXTS


def get_media_info(message: Message) -> tuple[Any, Optional[str]]:
    content_type = message.content_type
    media_obj = getattr(message, content_type, None)

    if isinstance(media_obj, list) and content_type == "photo":
        return media_obj[-1], content_type
    return media_obj, content_type


def format_id_output(message: Message, lang: str) -> str:
    t = TEXTS.get(lang, TEXTS["en"])
    media, c_type = get_media_info(message)

    header = f"🔍 <b>{c_type.upper()}</b>\n"
    divider = "—" * 20 + "\n"
    lines = []

    if hasattr(media, "file_id"):
        lines.append(f"🆔 <b>ID:</b> <code>{media.file_id}</code>")

    if hasattr(media, "file_size") and media.file_size:
        lines.append(f"⚖️ <b>{t['weight']}:</b> {media.file_size // 1024} KB")

    extra_data = _extract_extra_metadata(media, c_type, t)
    for key, value in extra_data.items():
        lines.append(f"🔹 <b>{key}:</b> {value}")

    if message.caption:
        lines.append(f"📝 <b>{t['caption']}:</b> {message.caption}")

    return f"{header}{divider}" + "\n".join(lines)


def _extract_extra_metadata(media: Any, c_type: str, t: Dict[str, str]) -> Dict[str, Any]:
    data = {}
    if c_type == "photo":
        data[t["size"]] = f"{media.width}x{media.height}"
    elif c_type in ["video", "animation"]:
        data[t["duration"]] = f"{media.duration} {t['sec']}"
        data[t["resolution"]] = f"{media.width}x{media.height}"
    elif c_type == "audio":
        data[t["performer"]] = media.performer or "N/A"
        data[t["track_title"]] = media.title or "N/A"
    elif c_type == "sticker":
        data[t["emoji"]] = media.emoji or "N/A"
    elif c_type == "contact":
        data[t["contact_id"]] = f"<code>{media.user_id}</code>"
        data[t["phone"]] = media.phone_number
    elif c_type == "location":
        data[t["coordinates"]] = f"{media.latitude}, {media.longitude}"
    elif c_type == "poll":
        data["ID"] = f"<code>{media.id}</code>"

    return data
