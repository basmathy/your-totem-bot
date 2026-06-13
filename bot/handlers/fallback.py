from datetime import datetime
from pathlib import Path

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.keyboards.inline import back_to_result_keyboard, restart_keyboard
from bot.quiz_data import TEXTS
from bot.states import get_session

router = Router()
REVIEWS_FILE = Path(__file__).resolve().parents[2] / "reviews.txt"


@router.callback_query(F.data == "result:review")
async def ask_review(callback: CallbackQuery) -> None:
    await callback.answer()
    session = get_session(callback.from_user.id)
    if not session or not session.get("result_animal_id"):
        await callback.message.answer(TEXTS["session_lost"], reply_markup=restart_keyboard())
        return

    session["state"] = "awaiting_review"
    await callback.message.answer(TEXTS["review_prompt"], reply_markup=back_to_result_keyboard())


@router.message(F.text)
async def process_text(message: Message) -> None:
    session = get_session(message.from_user.id)

    if not session:
        await message.answer(TEXTS["session_lost"], reply_markup=restart_keyboard())
        return

    if session.get("state") == "awaiting_review":
        REVIEWS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with REVIEWS_FILE.open("a", encoding="utf-8") as file:
            file.write(
                "\n".join(
                    [
                        f"[{datetime.now().isoformat(timespec='seconds')}]",
                        f"user_id={message.from_user.id}",
                        f"username=@{message.from_user.username or '-'}",
                        f"full_name={message.from_user.full_name}",
                        f"animal_id={session.get('result_animal_id')}",
                        f"review={message.text}",
                        "",
                    ]
                )
            )
        session["state"] = "result"
        await message.answer(TEXTS["review_saved"], reply_markup=back_to_result_keyboard())
        return

    if session.get("state") == "quiz":
        await message.answer(TEXTS["wrong_state"])
        return

    await message.answer(TEXTS["unknown_message"], reply_markup=restart_keyboard())


@router.callback_query()
async def process_unknown_callback(callback: CallbackQuery) -> None:
    await callback.answer()
    session = get_session(callback.from_user.id)
    if not session:
        await callback.message.answer(TEXTS["session_lost"], reply_markup=restart_keyboard())
        return
    await callback.message.answer(TEXTS["wrong_state"], reply_markup=restart_keyboard())
