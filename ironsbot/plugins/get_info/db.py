from collections.abc import Generator

import seerapi_models as seerapi_models
from nonebot import get_driver
from sqlalchemy.engine.base import Engine
from sqlmodel import Session as SQLModelSession
from sqlmodel import SQLModel, create_engine

from .config import plugin_config

_driver = get_driver()
_engine: Engine


@_driver.on_startup
async def init_orm() -> None:
    global _engine
    _engine = create_engine(plugin_config.database_url)
    SQLModel.metadata.create_all(_engine)


def get_engine() -> Engine | None:
    """获取数据库引擎实例。引擎未初始化时返回 None。"""
    try:
        return _engine
    except NameError:
        return None


def get_session() -> Generator[SQLModelSession, None, None]:
    with SQLModelSession(_engine) as session:
        yield session
