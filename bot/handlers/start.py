from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.inline import start_keyboard
from bot.quiz_data import TEXTS
from bot.states import reset_session

router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    reset_session(message.from_user.id)
    await message.answer(TEXTS["start"], reply_markup=start_keyboard())
