from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.quiz_data import BUTTONS
from bot.services.quiz_service import ANSWER_LABELS, get_current_question_answers


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BUTTONS["start_quiz"], callback_data="quiz:start")]
        ]
    )


def restart_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BUTTONS["start_again"], callback_data="quiz:restart")]
        ]
    )


def question_keyboard(session: dict) -> InlineKeyboardMarkup:
    answers = get_current_question_answers(session)
    buttons = [
        InlineKeyboardButton(
            text=ANSWER_LABELS[index],
            callback_data=f"answer:{answer['id']}",
        )
        for index, answer in enumerate(answers)
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BUTTONS["learn_guardianship"],
                    callback_data="result:guardianship",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BUTTONS["share_result"],
                    callback_data="result:share",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BUTTONS["contact_staff"],
                    callback_data="result:contact",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BUTTONS["leave_review"],
                    callback_data="result:review",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BUTTONS["restart_quiz"],
                    callback_data="quiz:restart",
                )
            ],
        ]
    )


def back_to_result_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=BUTTONS["back_to_result"],
                    callback_data="result:show",
                )
            ],
            [
                InlineKeyboardButton(
                    text=BUTTONS["restart_quiz"],
                    callback_data="quiz:restart",
                )
            ],
        ]
    )
