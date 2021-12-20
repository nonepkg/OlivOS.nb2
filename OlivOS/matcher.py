from nonebot import get_driver
from nonebot.adapters import Bot, Event
from nonebot.plugin import on_message, on_metaevent, on_notice, on_request

from OlivOS.middlewares import Proc
from OlivOS.middlewares.onebot import OlivOSEvent
from OlivOS.plugin import get_loaded_plugins, load_plugins

driver = get_driver()
message_matcher = on_message()
notice_matcher = on_notice()
request_matcher = on_request()
meta_matcher = on_metaevent()


@driver.on_startup
async def startup():
    load_plugins()


@driver.on_bot_connect
async def _(bot: Bot):
    for p in get_loaded_plugins():
        p.route.init(None, Proc())
    for p in get_loaded_plugins():
        p.route.init_after(None, Proc())


@message_matcher.handle()
async def _(bot: Bot, event: Event):
    for p in get_loaded_plugins():
        ovo_event = OlivOSEvent(bot, event)
        getattr(p.route, ovo_event.plugin_info["func_type"])(ovo_event, Proc())


@notice_matcher.handle()
async def _(bot: Bot, event: Event):
    for p in get_loaded_plugins():
        ovo_event = OlivOSEvent(bot, event)
        getattr(p.route, ovo_event.plugin_info["func_type"])(ovo_event, Proc())


@request_matcher.handle()
async def _(bot: Bot, event: Event):
    for p in get_loaded_plugins():
        ovo_event = OlivOSEvent(bot, event)
        getattr(p.route, ovo_event.plugin_info["func_type"])(ovo_event, Proc())


@meta_matcher.handle()
async def _(bot: Bot, event: Event):
    for p in get_loaded_plugins():
        ovo_event = OlivOSEvent(bot, event)
        getattr(p.route, ovo_event.plugin_info["func_type"])(ovo_event, Proc())


@driver.on_bot_disconnect
async def _(bot: Bot):
    for p in get_loaded_plugins():
        p.route.save(None, Proc())
