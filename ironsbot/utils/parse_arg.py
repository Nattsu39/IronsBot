from nonebot.adapters import Message
from nonebot.params import CommandArg, Depends


def parse_string_arg(args: Message = CommandArg()) -> str:
    arg = args.extract_plain_text()
    if not arg:
        raise ValueError("参数不能为空")
    return arg


def parse_int_arg(arg: str = Depends(parse_string_arg)) -> int:
    return int(arg)
