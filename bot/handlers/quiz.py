from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.keyboards.inline import question_keyboard, restart_keyboard
from bot.quiz_data import TEXTS
from bot.services.quiz_service import (
    apply_answer,
    choose_result_animal,
    create_quiz_state,
    find_answer,
    get_question_text,
    has_next_question,
)
from bot.states import get_session, user_sessions

router = Router()


async def send_first_question(callback: CallbackQuery) -> None:
    session = create_quiz_state()
    user_sessions[callback.from_user.id] = session
    await callback.message.answer(TEXTS["before_questions"])
    await callback.message.answer(
        get_question_text(session),
        reply_markup=question_keyboard(session),
    )


@router.callback_query(F.data.in_({"quiz:start", "quiz:restart"}))
async def start_quiz(callback: CallbackQuery) -> None:
    await callback.answer()
    if callback.data == "quiz:restart":
        await callback.message.answer(TEXTS["restart_confirm"])
    await send_first_question(callback)


@router.callback_query(F.data.startswith("answer:"))
async def process_answer(callback: CallbackQuery) -> None:
    await callback.answer()
    session = get_session(callback.from_user.id)

    if not session or session.get("state") != "quiz":
        await callback.message.answer(TEXTS["session_lost"], reply_markup=restart_keyboard())
        return

    answer_id = callback.data.split(":", 1)[1]
    answer = find_answer(session["question_index"], answer_id)
    if answer is None:
        await callback.message.answer(TEXTS["wrong_state"], reply_markup=restart_keyboard())
        return

    await callback.message.edit_text(
        get_question_text(session, selected_answer_id=answer_id),
        reply_markup=None,
    )

    apply_answer(session, answer)

    if has_next_question(session):
        await callback.message.answer(
            get_question_text(session),
            reply_markup=question_keyboard(session),
        )
        return

    animal_id = choose_result_animal(session["scores"])
    session["result_animal_id"] = animal_id
    session["state"] = "result"

    from bot.handlers.result import send_result

    await callback.message.answer(TEXTS["before_result"])
    await send_result(callback.message, animal_id)
