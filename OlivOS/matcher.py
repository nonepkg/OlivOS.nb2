from nonebot import get_driver
from nonebot.adapters import Bot, Event
from nonebot.plugin import on

from OlivOS.middlewares import Proc
from OlivOS.middlewares.onebot import OlivOSEvent
from OlivOS.plugin import get_loaded_plugins, load_plugins

driver = get_driver()
matcher = on()


@driver.on_startup
async def startup():
    load_plugins()


@driver.on_bot_connect
async def _(bot: Bot):
    for p in get_loaded_plugins():
        p.route.init(None, Proc())
    for p in get_loaded_plugins():
        p.route.init_after(None, Proc())


@matcher.handle()
async def _(bot: Bot, event: Event):
    for p in get_loaded_plugins():
        ovo_event = OlivOSEvent(bot, event)
        getattr(p.route, ovo_event.plugin_info["func_type"])(ovo_event, Proc())


@driver.on_bot_disconnect
async def _(bot: Bot):
    for p in get_loaded_plugins():
        p.route.save(None, Proc())
