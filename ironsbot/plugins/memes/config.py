from typing import Literal

from nonebot import get_plugin_config
from pydantic import BaseModel

MemeType = Literal["tudou", "pig", "capoo"]


class Config(BaseModel):
    memes_cnb_token: str | None = None
    memes_cnb_repo: str | None = None
    memes: frozenset[MemeType] = frozenset(["tudou", "pig", "capoo"])


plugin_config = get_plugin_config(Config)


def meme_is_enabled(meme_type: MemeType) -> bool:
    return meme_type in plugin_config.memes
