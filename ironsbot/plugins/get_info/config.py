from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel, arbitrary_types_allowed=True):
    database_url: str


plugin_config = get_plugin_config(Config)
