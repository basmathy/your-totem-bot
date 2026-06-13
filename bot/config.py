from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    bot_token: str
    contact_profile_url: str
    bot_link: str


def load_config() -> Config:
    load_dotenv()

    bot_token = getenv("BOT_TOKEN", "").strip()
    contact_profile_url = getenv("CONTACT_PROFILE_URL", "").strip()
    bot_link = getenv("BOT_LINK", "").strip()

    if not bot_token:
        raise RuntimeError("BOT_TOKEN не задан. Настройте .env по примеру из README.md.")

    if not contact_profile_url:
        raise RuntimeError(
            "CONTACT_PROFILE_URL не задан. Настройте .env по примеру из README.md."
        )

    if not bot_link:
        raise RuntimeError(
            "BOT_LINK не задан. Настройте .env по примеру из README.md."
        )

    return Config(
        bot_token=bot_token,
        contact_profile_url=contact_profile_url,
        bot_link=bot_link,
    )
