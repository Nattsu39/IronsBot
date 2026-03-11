from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    db_sync_url: str
    db_sync_interval_minutes: int = 60
    db_sync_path: str = "seerapi-data.sqlite"


plugin_config = get_plugin_config(Config)
