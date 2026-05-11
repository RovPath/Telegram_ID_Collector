from aiogram import Router, F
from aiogram.types import Message
from utils.formatter import format_id_output

router = Router()


@router.message(
    F.content_type.in_(
        {
            "photo",
            "video",
            "document",
            "audio",
            "voice",
            "video_note",
            "sticker",
            "animation",
            "poll",
            "contact",
            "location",
        }
    )
)
async def handle_any_media(message: Message, lang: str):
    text = format_id_output(message, lang)
    await message.reply(text=text)
