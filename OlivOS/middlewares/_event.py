from abc import ABC, abstractmethod
from typing import Callable, Optional

from nonebot.adapters import Bot, Event

from ._others import BotInfo


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
