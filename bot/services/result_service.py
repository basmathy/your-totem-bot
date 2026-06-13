from pathlib import Path

from aiogram.types import FSInputFile

from bot.quiz_data import ANIMALS, build_result_text, build_share_text


ANIMALS_DIR = Path(__file__).resolve().parents[1] / "animals"


def get_result_text(animal_id: str) -> str:
    animal = ANIMALS[animal_id]
    fact = animal.get("fact", "Это животное требует внимательной и регулярной заботы.")
    return (
        f"{build_result_text(animal_id)}\n\n"
        f"Реальный факт:\n{fact}\n\n"
        f"{animal['guardianship_text']}"
    )


def get_animal_photo(animal_id: str) -> FSInputFile | None:
    image_name = ANIMALS[animal_id]["image"]
    image_path = ANIMALS_DIR / image_name
    if not image_path.exists():
        return None
    return FSInputFile(image_path)


def get_share_text(animal_id: str, bot_link: str) -> str:
    return build_share_text(animal_id, bot_link)


def get_contact_message(animal_id: str) -> str:
    animal_name = ANIMALS[animal_id]["name"]
    return (
        "Здравствуйте! Я прошёл викторину «Какое у вас тотемное животное?» "
        f"и получил результат: {animal_name}. Хочу узнать больше о программе опеки "
        "Московского зоопарка."
    )
