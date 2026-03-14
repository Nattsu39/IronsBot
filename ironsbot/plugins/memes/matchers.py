import random
from collections.abc import AsyncGenerator, Callable
from dataclasses import dataclass
from typing import NoReturn

from nonebot import MatcherGroup, logger
from nonebot.adapters import Bot, Message, MessageTemplate
from nonebot.exception import FinishedException
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Depends
from nonebot_plugin_saa import Image

from ironsbot.utils.cnb import CnbApi
from ironsbot.utils.rule import no_reply

from .config import MemeType, meme_is_enabled, plugin_config

matcher_group = MatcherGroup()


def get_cnb_api(token: str, repo: str) -> Callable[[], AsyncGenerator[CnbApi, None]]:
    async def _get_cnb_api() -> AsyncGenerator[CnbApi, None]:
        async with CnbApi(token, repo=repo) as cnb:
            yield cnb

    return _get_cnb_api


@dataclass(frozen=True)
class ImageCommandConfig:
    """基于索引的图片命令配置。"""

    type: MemeType
    command: str
    aliases: set[str | tuple[str, ...]]
    max_index: int
    image_path_template: str
    message_template: MessageTemplate


def create_image_command(
    group: MatcherGroup,
    config: ImageCommandConfig,
    cnb_factory: Callable[..., AsyncGenerator[CnbApi, None]],
) -> type[Matcher]:
    """根据配置创建一个「随机/指定索引 + CnbApi 图片」的命令。"""
    matcher = group.on_command(config.command, aliases=config.aliases, rule=no_reply())
    if not meme_is_enabled(config.type):
        logger.warning(
            f"表情包【{config.type}】未启用，命令【{config.command}】将不会生效"
        )
        return matcher

    template = config.message_template

    async def _handler(
        m: Matcher,
        bot: Bot,
        arg: Message = CommandArg(),
        cnb: CnbApi = Depends(cnb_factory),
    ) -> NoReturn:
        is_random = False
        arg_str = arg.extract_plain_text()
        if arg_str.isdigit():
            index = int(arg_str)
        elif not arg_str:
            index = random.randint(1, config.max_index)
            is_random = True
        else:
            raise FinishedException

        if not 1 <= index <= config.max_index:
            await m.finish(f"编号必须在1到{config.max_index}之间！")

        image = Image(
            await cnb.get_file(config.image_path_template.format(index=index))
        )
        await m.finish(
            template.format(
                command=config.command,
                random_text="随机" if is_random else "自选",
                index=index,
                total=config.max_index,
                image=await image.build(bot),
            )
        )

    matcher.append_handler(_handler)
    return matcher


# ============ 命令配置 ============

DEFAULT_MESSAGE_TEMPLATE = MessageTemplate(
    "{random_text}{command}（{index}/{total}）\n"
    "🌈发【{command}x】直接出x号{command}，不加数字默认随机发送\n"
    "{image}"
)
COMMANDS: list[ImageCommandConfig] = []

if plugin_config.memes_cnb_token and plugin_config.memes_cnb_repo:
    _cnb_factory = get_cnb_api(
        plugin_config.memes_cnb_token, plugin_config.memes_cnb_repo
    )
    COMMANDS.append(
        ImageCommandConfig(
            type="tudou",
            command="土豆",
            aliases={"今日土豆", "随机土豆", "🥔"},
            max_index=2185,
            image_path_template="tudou/{index}.gif",
            message_template=DEFAULT_MESSAGE_TEMPLATE,
        )
    )
    COMMANDS.append(
        ImageCommandConfig(
            type="pig",
            command="小猪",
            aliases={"今日小猪", "随机小猪", "🐷", "🐖"},
            max_index=166,
            image_path_template="pig/{index}.jpg",
            message_template=DEFAULT_MESSAGE_TEMPLATE,
        )
    )

    for _cmd in COMMANDS:
        create_image_command(matcher_group, _cmd, _cnb_factory)

else:
    logger.warning("CNB 相关配置未设置，表情包命令将不会生效")
