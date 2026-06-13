from html import escape
from random import shuffle

from bot.quiz_data import ANIMAL_ORDER, QUESTIONS, get_empty_scores


ANSWER_LABELS = ("А", "Б", "В", "Г", "Д")


def create_answer_order() -> list[list[str]]:
    answer_order = []
    for question in QUESTIONS:
        answer_ids = [answer["id"] for answer in question["answers"]]
        shuffle(answer_ids)
        answer_order.append(answer_ids)
    return answer_order


def create_quiz_state() -> dict:
    return {
        "state": "quiz",
        "question_index": 0,
        "scores": get_empty_scores(),
        "answers": [],
        "answer_order": create_answer_order(),
        "result_animal_id": None,
    }


def get_ordered_answers(question_index: int, answer_order: list[list[str]]) -> list[dict]:
    question = QUESTIONS[question_index]
    answers_by_id = {answer["id"]: answer for answer in question["answers"]}

    if question_index >= len(answer_order):
        return question["answers"]

    return [
        answers_by_id[answer_id]
        for answer_id in answer_order[question_index]
        if answer_id in answers_by_id
    ]


def get_current_question_answers(session: dict) -> list[dict]:
    return get_ordered_answers(
        session["question_index"],
        session.get("answer_order", []),
    )


def get_question_text(session: dict, selected_answer_id: str | None = None) -> str:
    question_index = session["question_index"]
    question = QUESTIONS[question_index]
    current = question_index + 1
    total = len(QUESTIONS)
    ordered_answers = get_current_question_answers(session)
    answer_lines = []
    for index, answer in enumerate(ordered_answers):
        answer_line = f"{ANSWER_LABELS[index]}. {escape(answer['text'])}"
        if answer["id"] == selected_answer_id:
            answer_line = f"<b>{answer_line}</b>"
        answer_lines.append(answer_line)

    return (
        f"Вопрос {current}/{total}\n\n"
        f"{escape(question['text'])}\n\n"
        + "\n".join(answer_lines)
    )


def find_answer(question_index: int, answer_id: str) -> dict | None:
    question = QUESTIONS[question_index]
    for answer in question["answers"]:
        if answer["id"] == answer_id:
            return answer
    return None


def apply_answer(session: dict, answer: dict) -> None:
    for animal_id, points in answer["scores"].items():
        session["scores"][animal_id] = session["scores"].get(animal_id, 0) + points
    session["answers"].append(answer["id"])
    session["question_index"] += 1


def has_next_question(session: dict) -> bool:
    return session["question_index"] < len(QUESTIONS)


def choose_result_animal(scores: dict[str, int]) -> str:
    max_score = max(scores.values())
    for animal_id in ANIMAL_ORDER:
        if scores.get(animal_id) == max_score:
            return animal_id
    return ANIMAL_ORDER[0]
