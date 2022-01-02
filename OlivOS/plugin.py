import importlib
import inspect
import json
import shutil
import sys
import zipfile
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional, Set, Type

from nonebot.log import logger

from OlivOS.middlewares import OlivOSEvent, Proc, _middlewares


class Plugin:
    def __init__(self, conf: Dict[str, Any], module: ModuleType) -> None:
        self.name = conf["name"]
        self.author = conf["author"]
        self.namespace = conf["namespace"]
        self.message_mode = conf["message_mode"]
        self.priority = conf["priority"]
        self.support: Set[Type[OlivOSEvent]] = set()
        for middleware in _middlewares:
            for support in conf["support"]:
                if support["platform"] == "all" or middleware == support["platform"]:
                    self.support.add(_middlewares[middleware])
                    break
        self.route = Route(module.main.Event)


class Route:
    def __init__(self, event: object) -> None:
        for k, v in event.__dict__.items():
            if inspect.isfunction(v):
                setattr(self, k, v)

    def __getattr__(self, name: str):
        return self.default_handle

    def default_handle(
        self,
        plugin_event: Optional[OlivOSEvent] = None,
        proc: Optional[Proc] = None,
    ):
        pass


PLUGIN_PATH = "./data/OlivOS/app/"
PLUGIN_PATH_TMP = "./data/OlivOS/tmp/"
Path(PLUGIN_PATH).mkdir(parents=True, exist_ok=True)
Path(PLUGIN_PATH_TMP).mkdir(parents=True, exist_ok=True)
sys.path.append(PLUGIN_PATH)
sys.path.append(PLUGIN_PATH_TMP)

plugins: List[Plugin] = []


def get_loaded_plugins():
    return plugins


def load_plugins():
    for path in Path(PLUGIN_PATH).iterdir():
        try:
            if path.is_dir():
                module = importlib.import_module(path.stem)
            elif path.with_suffix(".opk"):
                zipfile.ZipFile(path).extractall(PLUGIN_PATH_TMP + path.stem)
                path = Path(PLUGIN_PATH_TMP + path.stem)
                module = importlib.import_module(path.stem)
            else:
                continue

            if hasattr(module, "main"):
                if hasattr(module.main, "Event"):
                    with (path / "app.json").open("r", encoding="utf-8") as f:
                        app_conf = json.load(f)
                    plugin = Plugin(app_conf, module)
                    plugins.append(plugin)
                    logger.opt(colors=True).success(f"[<e>{plugin.name}</e>] is loaded")
                    continue
                else:
                    skip_result = path.stem + ".main.Event" + " not found"
            else:
                skip_result = path.stem + ".main" + " not found"
            logger.opt(colors=True).error(
                f"<r><bg #f8bbd0>[{path.stem}] is skipped: {skip_result}</bg #f8bbd0></r>"
            )
        except Exception as e:
            logger.opt(colors=True).error(
                f"<r><bg #f8bbd0>[{path.stem}] is skipped: {e}</bg #f8bbd0></r>"
            )

    plugins.sort(key=lambda p: p.priority, reverse=True)

    for path in Path(PLUGIN_PATH).glob("*.opk"):
        shutil.rmtree(PLUGIN_PATH_TMP + path.stem, ignore_errors=True)
