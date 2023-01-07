from nonebot.plugin import on
from nonebot import get_driver
from nonebot.adapters import Bot, Event

from .middlewares import _middlewares, import_middleware
from .plugin import Proc, load_plugins, get_loaded_plugins

driver = get_driver()
matcher = on()


_proc = Proc()


@driver.on_startup
async def startup():
    import_middleware(*driver._adapters.keys())
    load_plugins()


@driver.on_bot_connect
async def _(bot: Bot):
    global _proc
    _proc = Proc()
    for p in get_loaded_plugins():
        p.route.init(None, _proc)
    for p in get_loaded_plugins():
        p.route.init_after(None, _proc)


@matcher.handle()
async def _(bot: Bot, event: Event):
    if bot.type.split(maxsplit=1)[0].lower() in _middlewares:
        ovo_event = _middlewares[bot.type.split(maxsplit=1)[0].lower()](bot, event)
        if ovo_event.plugin_info["func_type"]:
            for p in get_loaded_plugins():
                if type(ovo_event) in p.support:
                    getattr(p.route, ovo_event.plugin_info["func_type"])(
                        ovo_event, _proc
                    )


@driver.on_bot_disconnect
async def _(bot: Bot):
    global _proc
    _proc = Proc()
    for p in get_loaded_plugins():
        p.route.save(None, _proc)
