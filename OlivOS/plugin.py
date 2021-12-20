import importlib
import inspect
import json
import shutil
import sys
import zipfile
from pathlib import Path
from types import ModuleType
from typing import Dict, Optional

from nonebot.log import logger

from OlivOS.middlewares import OlivOSEvent, Proc


class Plugin:
    def __init__(self, name: str, module: ModuleType) -> None:
        self.route = Route(module.main.Event)


class Route:
    def __init__(self, event: object) -> None:
        for k, v in event.__dict__.items():
            if inspect.isfunction(v):
                setattr(self, k, v)

    def __getattr__(self, name: str):
        return self.handle

    def handle(
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

plugins: Dict[str, Plugin] = {}


def get_loaded_plugins():
    return plugins.values()


def load_plugins():
    # 解包 opk
    for plugin in Path(PLUGIN_PATH).glob("*.opk"):
        zipfile.ZipFile(plugin).extractall(PLUGIN_PATH_TMP + plugin.stem)

    for plugin in Path(PLUGIN_PATH).iterdir():
        if plugin.is_dir():
            plugin_models = importlib.import_module(plugin.stem)
        elif plugin.with_suffix(".opk"):
            plugin = Path(PLUGIN_PATH_TMP + plugin.stem)
            plugin_models = importlib.import_module(plugin.stem)
        else:
            continue

        if hasattr(plugin_models, "main"):
            if hasattr(plugin_models.main, "Event"):
                with (plugin / "app.json").open("r", encoding="utf-8") as f:
                    app_conf = json.load(f)
                plugins[app_conf["name"]] = Plugin("", plugin_models)
                logger.opt(colors=True).success(
                    f"[<e>{app_conf['name']}</e>] is loaded"
                )
                continue
            else:
                skip_result = plugin.stem + ".main.Event" + " not found"
        else:
            skip_result = plugin.stem + ".main" + " not found"
        logger.opt(colors=True).error(
            f"<r><bg #f8bbd0>[{plugin.stem}] is skipped: {skip_result}</bg #f8bbd0></r>"
        )

    for plugin in Path(PLUGIN_PATH).glob("*.opk"):
        shutil.rmtree(PLUGIN_PATH_TMP + plugin.stem)
