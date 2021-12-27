import asyncio
from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Optional

from nonebot import get_bot
from nonebot.adapters import Bot, Event

from ._others import ID, MSG, BotInfo, Result


class OlivOSEvent(ABC):
    def __init__(
        self,
        bot: Optional[Bot] = None,
        event: Optional[Event] = None,
        log_func: Optional[Callable] = None,
    ):
        self.platform = {}
        self.platform["sdk"] = None
        self.platform["platform"] = None
        self.platform["model"] = None
        self.data = None
        self.active = False
        self.blocked = False
        self.log_func = log_func
        self.base_info = {}
        self.base_info["time"] = None
        self.base_info["self_id"] = None
        self.base_info["type"] = None
        self.plugin_info = {}
        self.plugin_info["func_type"] = None
        self.plugin_info[
            "message_mode_rx"
        ] = "old_string"  # OlivOS_message_mode_rx_default
        self.plugin_info[
            "message_mode_tx"
        ] = "olivos_string"  # OlivOS_message_mode_rx_default
        self.plugin_info["name"] = "unity"
        self.plugin_info["namespace"] = "unity"
        self.plugin_info["tx_queue"] = []
        if bot:
            if isinstance(bot, Bot):
                self.platform = {"sdk": "onebot", "platform": "qq", "model": "nonebot"}
            self.bot_info = BotInfo(int(bot.self_id), self.platform)
        if event:
            self.get_Event_from_SDK(event)
        # TODO self.get_Event_on_Plugin()

    @abstractmethod
    def get_Event_from_SDK(self, event: Event):
        raise NotImplementedError

    """
    TODO
    def get_Event_on_Plugin(self):
        if self.plugin_info["func_type"] in ["private_message", "group_message"]:
            if self.data.message_sdk.mode_rx == self.plugin_info["message_mode_tx"]:
                self.data.message = self.data.message_sdk.data_raw
            else:
                self.data.message = self.data.message_sdk.get(
                    self.plugin_info["message_mode_tx"]
                )
            if self.data.raw_message_sdk.mode_rx == self.plugin_info["message_mode_tx"]:
                self.data.raw_message = self.data.raw_message_sdk.data_raw
            else:
                self.data.raw_message = self.data.raw_message_sdk.get(
                    self.plugin_info["message_mode_tx"]
                )
    """

    def run_async(self, func: Awaitable):
        task = asyncio.create_task(func)
        if task.done():
            return task.result()
        else:
            return None

    def set_block(self):
        pass

    def call_api(self, api: str, **kwargs):
        result = self.run_async(get_bot(str(self.bot_info.id)).call_api(api, **kwargs))
        if result:
            return Result(True, result)
        else:
            return Result()

    @abstractmethod
    def reply(self, message: MSG):
        raise NotImplementedError

    @abstractmethod
    def send(self, send_type: str, target_id: ID, message: MSG):
        raise NotImplementedError

    @abstractmethod
    def delete_msg(self, message_id: ID):
        raise NotImplementedError

    @abstractmethod
    def get_msg(self, message_id: ID):
        raise NotImplementedError

    @abstractmethod
    def send_like(self, user_id: ID):
        raise NotImplementedError

    @abstractmethod
    def set_group_kick(self, group_id: ID, user_id: ID):
        raise NotImplementedError

    @abstractmethod
    def set_group_ban(self, group_id: ID, user_id: ID):
        raise NotImplementedError

    @abstractmethod
    def set_group_whole_ban(self, group_id: ID, enable: bool):
        raise NotImplementedError

    @abstractmethod
    def set_group_admin(self, group_id: ID, user_id: ID, enable: bool):
        raise NotImplementedError

    @abstractmethod
    def set_group_card(self, group_id: ID, user_id: ID, card: str):
        raise NotImplementedError

    @abstractmethod
    def set_group_name(self, group_id: ID, group_name: str):
        raise NotImplementedError

    @abstractmethod
    def set_group_leave(self, group_id: ID):
        raise NotImplementedError

    @abstractmethod
    def set_group_special_title(
        self, group_id: ID, user_id: ID, special_title: str, duration: int
    ):
        raise NotImplementedError

    @abstractmethod
    def set_friend_add_request(self, flag: ID, approve: bool, remark: str):
        raise NotImplementedError

    @abstractmethod
    def set_group_add_request(self, flag: ID, sub_type: str, approve: bool, reason):
        raise NotImplementedError

    @abstractmethod
    def get_login_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_stranger_info(self, user_id: ID):
        raise NotImplementedError

    @abstractmethod
    def get_friend_list(self):
        raise NotImplementedError

    @abstractmethod
    def get_group_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_group_list(self):
        raise NotImplementedError

    @abstractmethod
    def get_group_member_info(self):
        raise NotImplementedError

    @abstractmethod
    def get_group_member_list(self):
        raise NotImplementedError
