from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.config import Config
from bot.keyboards.inline import back_to_result_keyboard, restart_keyboard
from bot.quiz_data import TEXTS
from bot.services.result_service import get_contact_message
from bot.states import get_session

router = Router()


@router.callback_query(F.data == "result:contact")
async def contact_staff(callback: CallbackQuery, config: Config) -> None:
    await callback.answer()
    session = get_session(callback.from_user.id)
    animal_id = session.get("result_animal_id") if session else None

    if not animal_id:
        await callback.message.answer(TEXTS["session_lost"], reply_markup=restart_keyboard())
        return

    await callback.message.answer(
        TEXTS["contact_profile"].format(
            contact_profile_url=config.contact_profile_url,
            contact_message=get_contact_message(animal_id),
        ),
        reply_markup=back_to_result_keyboard(),
    )
