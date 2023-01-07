import asyncio
import hashlib
import importlib
from abc import ABC, abstractmethod
from typing import Dict, Type, Union, Callable, Optional, Awaitable

from pydantic import BaseModel

from nonebot import get_bot
from nonebot.log import logger
from nonebot.adapters import Bot, Event

middlewares_map = {"onebot": "onebot", "telegram": "telegram"}
sdk_map = {"onebot": "onebot", "telegram": "telegram"}
platform_map = {"onebot": "qq", "telegram": "telegram"}

_middlewares: Dict[str, Type["OlivOSEvent"]] = {}


def import_middleware(*adapters):
    for adapter in adapters:
        adapter = adapter.split(maxsplit=1)[0].lower()
        if adapter in middlewares_map:
            module = importlib.import_module(
                f"OlivOS.nonebot.middlewares.{middlewares_map[adapter]}"
            )

            _middlewares[adapter] = getattr(module, "OlivOSEvent")
        else:
            logger.warning(f"Can not find middleware for Adapter {adapter}")


ID = Union[int, str]

MSG = str


class Result:
    def __init__(self, active: bool = False, data: Optional[dict] = None):
        self.active = active
        self.data = data


class BotInfo:
    sdk_map = {}
    platform_map = {}

    def __init__(self, bot: Bot) -> None:
        self.id = bot.self_id
        self.platform = {"model": "nonebot"}
        type = bot.type.split(maxsplit=1)[0].lower()
        self.platform["sdk"] = sdk_map.get(type, type)
        self.platform["platform"] = platform_map.get(type, type)

        hash_tmp = hashlib.new("md5")
        hash_tmp.update(str(self.id).encode(encoding="UTF-8"))
        hash_tmp.update(str(self.platform["sdk"]).encode(encoding="UTF-8"))
        hash_tmp.update(str(self.platform["platform"]).encode(encoding="UTF-8"))
        # hash_tmp.update(str(self.platform["model"]).encode(encoding='UTF-8'))
        self.hash = hash_tmp.hexdigest()


class OlivOSEvent(ABC):
    bot_info: BotInfo
    data: "Data"

    class Data(BaseModel):
        def __getattr__(self, name):
            return None

        class Config:
            extra = "allow"

    def __init__(
        self,
        bot: Optional[Bot] = None,
        event: Optional[Event] = None,
        log_func: Optional[Callable] = None,
    ):
        self.platform = {"sdk": None, "platform": None, "model": None}
        self.active = False
        self.blocked = False

        self.log_func = log_func

        self.base_info = {"time": None, "self_id": None, "type": None}
        self.plugin_info = {
            "func_type": None,
            "message_mode_rx": "old_string",  # OlivOS_message_mode_rx_default
            "message_mode_tx": "olivos_string",  # OlivOS_message_mode_rx_default
            "name": "unity",
            "namespace": "unity",
            "tx_queue": [],
        }

        if bot:
            self.process_bot(bot)

        if event:
            self.process_event(event)

        self.process_message()

    @abstractmethod
    def process_bot(self, bot: Bot):
        raise NotImplementedError

    @abstractmethod
    def process_event(self, event: Event):
        raise NotImplementedError

    def process_message(self):
        if self.plugin_info["func_type"] in ["private_message", "group_message"]:
            if (
                self.data.message_sdk.mode_rx  # type:ignore
                == self.plugin_info["message_mode_tx"]
            ):
                self.data.message = self.data.message_sdk.data_raw  # type:ignore
            else:
                self.data.message = self.data.message_sdk.get(  # type:ignore
                    self.plugin_info["message_mode_tx"]
                )
            if (
                self.data.raw_message_sdk.mode_rx  # type:ignore
                == self.plugin_info["message_mode_tx"]
            ):
                self.data.raw_message = (
                    self.data.raw_message_sdk.data_raw  # type:ignore
                )
            else:
                self.data.raw_message = self.data.raw_message_sdk.get(  # type:ignore
                    self.plugin_info["message_mode_tx"]
                )

    def run_async(self, func: Awaitable):
        task = asyncio.create_task(func)
        if task.done():
            return task.result()
        else:
            return None

    def set_block(self):
        pass

    def call_api(self, api: str, **kwargs) -> Result:
        result = self.run_async(get_bot(str(self.bot_info.id)).call_api(api, **kwargs))
        if result:
            return Result(True, result)
        else:
            return Result()

    @abstractmethod
    def reply(self, message: MSG):
        raise NotImplementedError

    def send(self, send_type: str, target_id: ID, message: MSG):
        raise NotImplementedError

    def delete_msg(self, message_id: ID):
        raise NotImplementedError

    def get_msg(self, message_id: ID) -> Result:
        raise NotImplementedError

    def send_like(self, user_id: ID):
        raise NotImplementedError

    def set_group_kick(self, group_id: ID, user_id: ID):
        raise NotImplementedError

    def set_group_ban(self, group_id: ID, user_id: ID):
        raise NotImplementedError

    def set_group_whole_ban(self, group_id: ID, enable: bool):
        raise NotImplementedError

    def set_group_admin(self, group_id: ID, user_id: ID, enable: bool):
        raise NotImplementedError

    def set_group_card(self, group_id: ID, user_id: ID, card: str):
        raise NotImplementedError

    def set_group_name(self, group_id: ID, group_name: str):
        raise NotImplementedError

    def set_group_leave(self, group_id: ID):
        raise NotImplementedError

    def set_group_special_title(
        self, group_id: ID, user_id: ID, special_title: str, duration: int
    ):
        raise NotImplementedError

    def set_friend_add_request(self, flag: ID, approve: bool, remark: str):
        raise NotImplementedError

    def set_group_add_request(self, flag: ID, sub_type: str, approve: bool, reason):
        raise NotImplementedError

    def get_login_info(self) -> Result:
        raise NotImplementedError

    def get_stranger_info(self, user_id: ID) -> Result:
        raise NotImplementedError

    def get_friend_list(self) -> Result:
        raise NotImplementedError

    def get_group_info(self) -> Result:
        raise NotImplementedError

    def get_group_list(self) -> Result:
        raise NotImplementedError

    def get_group_member_info(self) -> Result:
        raise NotImplementedError

    def get_group_member_list(self) -> Result:
        raise NotImplementedError
