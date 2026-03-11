import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

app = nonebot.get_asgi()

# driver.register_adapter(CONSOLE_Adapter)
# nonebot.load_builtin_plugins("echo")
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run(host="127.0.0.1", port=8080, app=app)
