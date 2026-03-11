import asyncio
import sqlite3
from pathlib import Path

import httpx
from nonebot import get_driver, require
from nonebot.log import logger

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

from .config import plugin_config

_SQLITE_MAGIC = b"SQLite format 3\x00"

_driver = get_driver()
_sync_lock = asyncio.Lock()


def _dispose_existing_engine() -> None:
    """释放 get_info 插件持有的数据库连接池，以便安全替换文件。"""
    try:
        from ironsbot.plugins.get_info.db import get_engine

        engine = get_engine()
        if engine is not None:
            engine.dispose()
            logger.debug("已释放数据库连接池")
    except ImportError:
        logger.debug("get_info 插件未加载，跳过连接释放")


def _validate_sqlite(path: Path) -> None:
    """校验下载的文件是否为合法的 SQLite 数据库。"""
    with path.open("rb") as f:
        header = f.read(16)
    if not header.startswith(_SQLITE_MAGIC):
        msg = "下载的文件不是有效的 SQLite 数据库"
        raise ValueError(msg)

    with sqlite3.connect(str(path)) as conn:
        conn.execute("SELECT 1")


async def sync_database() -> None:
    """从远程 URL 下载 SQLite 数据库并替换本地文件。"""
    url = plugin_config.db_sync_url
    if not url:
        return

    async with _sync_lock:
        db_path = Path(plugin_config.db_sync_path)
        tmp_path = db_path.with_suffix(".db.tmp")

        logger.info(f"开始从 {url} 同步数据库...")

        try:
            async with (
                httpx.AsyncClient(
                    follow_redirects=True,
                    timeout=httpx.Timeout(30.0, read=120.0),
                ) as client,
                client.stream("GET", url) as response,
            ):
                response.raise_for_status()
                with tmp_path.open("wb") as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)

            _validate_sqlite(tmp_path)
            _dispose_existing_engine()
            tmp_path.replace(db_path)

            stat_result = await asyncio.to_thread(db_path.stat)
            size_mb = stat_result.st_size / (1024 * 1024)
            logger.info(f"数据库同步完成，文件大小: {size_mb:.2f} MB")

        except httpx.HTTPError:
            logger.exception("数据库同步失败（HTTP 错误）")
            tmp_path.unlink(missing_ok=True)
        except (OSError, ValueError):
            logger.exception("数据库同步失败（文件校验或 IO 错误）")
            tmp_path.unlink(missing_ok=True)


if plugin_config.db_sync_url:
    scheduler.add_job(
        sync_database,
        "interval",
        minutes=plugin_config.db_sync_interval_minutes,
        id="db_sync",
        replace_existing=True,
    )


@_driver.on_startup
async def _on_startup() -> None:
    if not plugin_config.db_sync_url:
        logger.debug("db_sync_url 未配置，数据库同步插件未激活")
        return

    logger.info(
        f"数据库同步插件已启动，同步间隔: {plugin_config.db_sync_interval_minutes} 分钟"
    )
    await sync_database()
