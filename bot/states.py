from typing import Any


UserSession = dict[str, Any]

user_sessions: dict[int, UserSession] = {}


def reset_session(user_id: int) -> UserSession:
    session: UserSession = {
        "state": "ready",
        "question_index": 0,
        "scores": {},
        "answers": [],
        "answer_order": [],
        "result_animal_id": None,
    }
    user_sessions[user_id] = session
    return session


def get_session(user_id: int) -> UserSession | None:
    return user_sessions.get(user_id)
