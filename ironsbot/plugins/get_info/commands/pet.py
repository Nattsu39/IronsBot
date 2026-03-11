from nonebot import on_command
from nonebot.adapters import Message, MessageTemplate
from nonebot.adapters.onebot.v11 import Message as OneBotV11Message
from nonebot.adapters.onebot.v11 import MessageSegment as OneBotV11MessageSegment
from nonebot.exception import FinishedException
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot.typing import T_State
from seerapi_models import PetORM, PetSkinORM

from ironsbot.plugins.get_info.prompt import (
    PROMPT_STATE_KEY,
    Prompt,
    PromptItem,
    create_prompt_got_handler,
    simple_prompt_resolver,
)

from ..depends import GetPetData, GetPetSkinData, PetBodyImageGetter, PetDataGetter
from ..render import render_pet_info

pet_image_matcher = on_command("立绘", rule=to_me(), priority=3, block=True)


PROMPT_MAX_ITEMS = 20


@pet_image_matcher.handle()
async def handle_pet_image(
    matcher: Matcher,
    state: T_State,
    pets: list[PetORM] = GetPetData(),
    skins: list[PetSkinORM] = GetPetSkinData(),
) -> None:
    _name_set: set[str] = set()
    items: list[PromptItem[int]] = [
        PromptItem(name=pet.name, desc=str(pet.id), value=pet.id) for pet in pets
    ]
    items.extend(
        PromptItem(
            name=skin.name, desc=f"所属精灵：{skin.pet.name}", value=skin.resource_id
        )
        for skin in skins
    )

    if not items:
        raise FinishedException

    if len(items) == 1:
        await matcher.finish(await build_pet_image_message(items[0]))

    if len(pets) > PROMPT_MAX_ITEMS:
        await matcher.finish(f"重名超过{PROMPT_MAX_ITEMS}个，请重新检索关键词！")

    state[PROMPT_STATE_KEY] = Prompt(
        title="请问你想查询的立绘是……",
        items=items,
    )
    state["prompt_message"] = state[PROMPT_STATE_KEY].build_message()


async def build_pet_image_message(args: PromptItem[int]) -> Message:
    image = await PetBodyImageGetter(str(args.value), cls=OneBotV11MessageSegment)
    msg = OneBotV11Message()
    msg += f"💎{args.name}\n"
    msg += image
    return msg


async def pet_image_resolver(
    item: PromptItem[int], matcher: Matcher, _: object
) -> None:
    await matcher.finish(await build_pet_image_message(item))


PET_IMAGE_GOT_KEY = "pet_image"
pet_image_matcher.got(PET_IMAGE_GOT_KEY, prompt=MessageTemplate("{prompt_message}"))(
    create_prompt_got_handler(PET_IMAGE_GOT_KEY, pet_image_resolver)
)


# ============ 精灵信息卡 ============

pet_info_matcher = on_command("精灵", rule=to_me(), priority=3, block=True)


@pet_info_matcher.handle()
async def handle_pet_info(
    matcher: Matcher,
    state: T_State,
    pets: list[PetORM] = GetPetData(),
    # aliases: list[PetORM] = GetPetData(),
) -> None:
    if not pets:
        raise FinishedException

    if len(pets) == 1:
        await matcher.finish(await build_pet_info_message(pets[0]))

    if len(pets) > PROMPT_MAX_ITEMS:
        await matcher.finish(f"重名超过{PROMPT_MAX_ITEMS}个，请重新检索关键词！")

    state[PROMPT_STATE_KEY] = Prompt(
        title="请问你想查询的精灵是……",
        items=[
            PromptItem(name=pet.name, desc=str(pet.id), value=pet.id) for pet in pets
        ],
    )
    state["prompt_message"] = state[PROMPT_STATE_KEY].build_message()


async def build_pet_info_message(pet: PetORM) -> Message:
    pic_bytes = await render_pet_info(pet)
    msg = OneBotV11Message()
    msg += OneBotV11MessageSegment.image(pic_bytes)
    return msg


PET_INFO_GOT_KEY = "pet_info"
pet_info_matcher.got(PET_INFO_GOT_KEY, prompt=MessageTemplate("{prompt_message}"))(
    create_prompt_got_handler(
        PET_INFO_GOT_KEY,
        simple_prompt_resolver(PetDataGetter, build_pet_info_message, "精灵"),
    )
)
