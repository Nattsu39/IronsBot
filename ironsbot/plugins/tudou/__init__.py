from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import Bot

tudou = on_fullmatch("土豆", priority=3)


@tudou.handle()
async def test(bot: Bot):
    await tudou.finish("土豆")
