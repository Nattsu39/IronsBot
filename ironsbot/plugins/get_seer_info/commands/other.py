from datetime import timedelta, timezone
from typing import NoReturn

from nonebot.adapters import Bot, MessageTemplate
from nonebot.matcher import Matcher
from seerapi_models import ApiMetadataORM
from sqlmodel import select

from ironsbot.utils.rule import no_reply

from ..depends import Session
from ..depends.image import PreviewImageGetter
from ..group import matcher_group

preview_matcher = matcher_group.on_fullmatch("下周预告", rule=no_reply())

PREVIEW_MESSAGE_TEMPLATE = MessageTemplate(
    "{image}\n预告图来自 https://github.com/WhY15w/seer-unity-preview-img-dumper"
)


@preview_matcher.handle()
async def handle_preview(matcher: Matcher, bot: Bot) -> NoReturn:
    image = await PreviewImageGetter.get("")
    await matcher.finish(PREVIEW_MESSAGE_TEMPLATE.format(image=await image.build(bot)))


data_version_matcher = matcher_group.on_fullmatch("数据版本", rule=no_reply())

DATA_VERSION_MESSAGE_TEMPLATE = MessageTemplate("数据更新时间：{time}")


@data_version_matcher.handle()
async def handle_data_version(matcher: Matcher, session: Session) -> NoReturn:
    obj = session.exec(select(ApiMetadataORM)).first()
    if not obj:
        await matcher.finish("❌暂无数据版本信息(这是一个bug，请反馈给开发者)")
    dt = obj.generate_time
    dt_local = dt.astimezone(timezone(timedelta(hours=8)))
    time = dt_local.strftime("%Y-%m-%d %H:%M:%S")
    await matcher.finish(DATA_VERSION_MESSAGE_TEMPLATE.format(time=time))
