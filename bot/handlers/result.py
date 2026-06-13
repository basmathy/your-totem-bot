from html import escape

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.config import Config
from bot.keyboards.inline import back_to_result_keyboard, result_keyboard, restart_keyboard
from bot.quiz_data import ANIMALS, TEXTS
from bot.services.result_service import get_animal_photo, get_result_text, get_share_text
from bot.states import get_session

router = Router()


async def send_result(message: Message, animal_id: str) -> None:
    photo = get_animal_photo(animal_id)
    text = get_result_text(animal_id)

    if photo:
        await message.answer_photo(photo=photo)
        await message.answer(text, reply_markup=result_keyboard())
        return

    await message.answer(text, reply_markup=result_keyboard())
    await message.answer(
        TEXTS["photo_missing"].format(image_name=ANIMALS[animal_id]["image"])
    )


def get_result_animal_or_none(user_id: int) -> str | None:
    session = get_session(user_id)
    if not session or session.get("state") not in {"result", "awaiting_review"}:
        return None
    return session.get("result_animal_id")


@router.callback_query(F.data == "result:show")
async def show_result(callback: CallbackQuery) -> None:
    await callback.answer()
    animal_id = get_result_animal_or_none(callback.from_user.id)
    if not animal_id:
        await callback.message.answer(TEXTS["session_lost"], reply_markup=restart_keyboard())
        return
    await send_result(callback.message, animal_id)


@router.callback_query(F.data == "result:guardianship")
async def show_guardianship(callback: CallbackQuery) -> None:
    await callback.answer()
    if not get_result_animal_or_none(callback.from_user.id):
        await callback.message.answer(TEXTS["session_lost"], reply_markup=restart_keyboard())
        return
    await callback.message.answer(
        TEXTS["guardianship_full"],
        reply_markup=back_to_result_keyboard(),
    )


@router.callback_query(F.data == "result:share")
async def show_share_text(callback: CallbackQuery, config: Config) -> None:
    await callback.answer()
    animal_id = get_result_animal_or_none(callback.from_user.id)
    if not animal_id:
        await callback.message.answer(TEXTS["session_lost"], reply_markup=restart_keyboard())
        return

    share_text = escape(get_share_text(animal_id, config.bot_link))
    await callback.message.answer(
        f"{TEXTS['share_instruction']}\n\n<pre>{share_text}</pre>",
        reply_markup=back_to_result_keyboard(),
    )
