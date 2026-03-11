import httpx
from nonebot.adapters import MessageSegment
from nonebot.params import Depends

from .parse_arg import parse_string_arg


def create_image_segment(
    img_bytes: bytes,
    *,
    cls: type[MessageSegment],
) -> MessageSegment:
    return cls.image(img_bytes)


async def create_image_segment_from_url(
    url: str, *, cls: type[MessageSegment]
) -> MessageSegment:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return create_image_segment(response.content, cls=cls)


class GetImage:
    def __init__(self, url_template: str) -> None:
        self.url_template = url_template

    async def __call__(
        self,
        arg: str = Depends(parse_string_arg),
        *,
        cls: type[MessageSegment],
    ) -> MessageSegment:
        url = self.url_template.format(arg)
        try:
            return await create_image_segment_from_url(url, cls=cls)
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            reason_phrase = e.response.reason_phrase
            return cls.text(f"❌获取图片失败！原因：{status_code} {reason_phrase}")
