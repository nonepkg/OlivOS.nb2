"""
https://github.com/OlivOS-Team/OlivOS/blob/main/OlivOS/telegramSDK.py
"""

from typing import Dict, Type, Optional

from OlivOS.messageAPI import Message_templet

from nonebot import get_bot
from nonebot.adapters.telegram.bot import Bot
from nonebot.adapters.telegram.message import Message
from nonebot.adapters.telegram.event import *  # type:ignore

from . import MSG, BotInfo
from . import OlivOSEvent as BaseOlivOSEvent


class OlivOSEvent(BaseOlivOSEvent):
    def process_bot(self, bot: Bot):
        self.platform = {"sdk": "telegram", "platform": "telegram", "model": "nonebot"}
        self.bot_info = BotInfo(bot)
        self.base_info["self_id"] = bot.self_id

    def process_event(self, event: Event):
        self.data = self.Data(**event.dict())

        self.base_info["time"] = event.date  # type:ignore
        self.base_info["type"] = event.get_type()

        self.plugin_info["message_mode_rx"] = "old_string"

        func_type_map: Dict[Type[Event], Optional[str]] = {
            PrivateMessageEvent: "private_message",
            GroupMessageEvent: "group_message",
        }
        if type(event) in func_type_map:
            self.active = True
            self.plugin_info["func_type"] = func_type_map[type(event)]
        if isinstance(event, MessageEvent):
            self.data.sender = {
                "nickname": event.from_.first_name,
                "user_id": event.from_.id,
                "name": event.from_.first_name,
                "id": event.from_.id,
            }

            self.data.extend = {}
            message = Message_templet("old_string", str(event.message))
            self.data.raw_message = message
            self.data.message_sdk = message
            self.data.raw_message_sdk = message

    def reply(self, message: MSG):
        if self.data:
            self.run_async(
                get_bot(str(self.bot_info.id)).send(
                    MessageEvent(**self.data.dict()), Message(message)
                )
            )

    def send(self, message: MSG):
        self.call_api(
            "sendMessage", chat_id=self.data.chat.id, text=message  # type:ignore
        )
