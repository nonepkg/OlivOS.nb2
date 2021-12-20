import asyncio
from typing import Callable, Dict, Optional, Type

from nonebot import get_bots
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import *
from nonebot.adapters.cqhttp.message import Message

from OlivOS.middlewares import BotInfo
from OlivOS.middlewares import OlivOSEvent as BaseOlivOSEvent


class OlivOSEvent(BaseOlivOSEvent):
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
        # self.get_Event_on_Plugin()

    def get_Event_from_SDK(self, event: Event):
        self.data = event.copy()
        self.base_info["time"] = event.time
        self.base_info["self_id"] = event.self_id
        self.base_info["type"] = event.post_type
        self.base_info["sdk"] = "onebot"
        self.base_info["platform"] = "qq"
        self.base_info["model"] = "nonebot"
        self.plugin_info["message_mode_rx"] = "old_string"
        func_type_map: Dict[Type[Event], Optional[str]] = {
            PrivateMessageEvent: "private_message",
            GroupMessageEvent: "group_message",
            GroupUploadNoticeEvent: "group_file_upload",
            GroupAdminNoticeEvent: "group_admin",
            GroupDecreaseNoticeEvent: "group_member_decrease",
            GroupIncreaseNoticeEvent: "group_member_increase",
            GroupBanNoticeEvent: "group_ban",
            FriendAddNoticeEvent: "friend_add",
            GroupRecallNoticeEvent: "group_message_recall",
            FriendRecallNoticeEvent: "private_message_recall",
            PokeNotifyEvent: "poke",
            LuckyKingNotifyEvent: "group_lucky_king",
            HonorNotifyEvent: "group_honor",
            FriendRequestEvent: "friend_add_request",
            GroupRequestEvent: None,
            LifecycleMetaEvent: "lifecycle",
            HeartbeatMetaEvent: "heartbeat",
        }
        if type(event) in func_type_map:
            self.data.active = True
            self.plugin_info["func_type"] = func_type_map[type(event)]
        if isinstance(event, MessageEvent):
            self.data.message = event.raw_message
            self.data.sender = event.sender.dict()
            self.data.extend = {}
            # self.data.message_sdk = OlivOS.messageAPI.Message_templet(
            #     "old_string", str(event.message)
            # )
            # self.data.raw_message_sdk = OlivOS.messageAPI.Message_templet(
            #     "old_string", event.raw_message
            # )
            if isinstance(event, GroupMessageEvent):
                self.data.host_id = None
                if event.sub_type != "normal":
                    self.active = False
            # TODO GuildEvent
            # elif event.message_type == "guild":
            #     if event.sub_type == "channel":
            #         self.active = True
            #         self.plugin_info["func_type"] = "group_message"
            #         if "guild_id" in self.sdk_event.json:
            #             self.data.host_id = event.guild_id
            #             self.data.extend["host_group_id"] = self.sdk_event.json[
            #                 "guild_id"
            #             ]
            #         if "self_tiny_id" in self.sdk_event.json:
            #             self.data.extend["sub_self_id"] = self.sdk_event.json[
            #                 "self_tiny_id"
            #             ]
            #             if event.user_id == event.self_tiny_id:
            #                 self.active = False
            if event.raw_message == "":
                self.active = False
        elif isinstance(event, NoticeEvent):
            if isinstance(event, GroupUploadNoticeEvent):
                self.data.file = event.file.dict()
            elif isinstance(
                event,
                (
                    GroupAdminNoticeEvent,
                    GroupDecreaseNoticeEvent,
                    GroupIncreaseNoticeEvent,
                    GroupBanNoticeEvent,
                ),
            ):
                self.data.action = event.sub_type
            elif isinstance(event, GroupBanNoticeEvent):
                self.active = True
                self.data.action = {"ban": "ban", "lift_ban": "unban"}[event.sub_type]
            elif isinstance(event, NotifyEvent):
                if isinstance(event, PokeNotifyEvent):
                    if not event.group_id:
                        self.data.group_id = -1
                elif isinstance(event, HonorNotifyEvent):
                    self.active = True
                    self.data.type = event.honor_type
        elif isinstance(event, (GroupRequestEvent, FriendRequestEvent)):
            if not event.comment:
                self.data.comment = ""
            if isinstance(event, GroupRequestEvent):
                if event.sub_type == "add":
                    self.plugin_info["func_type"] = "group_add_request"
                elif event.sub_type == "invite":
                    self.plugin_info["func_type"] = "group_invite_request"
        elif isinstance(event, MetaEvent):
            if isinstance(event, LifecycleMetaEvent):
                self.data.action = event.sub_type

    def set_group_leave(self, group_id: int):
        asyncio.create_task(
            get_bots()[str(self.bot_info.id)].set_group_leave(group_id=group_id)
        )

    def set_friend_add_request(self, flag: str, approve: bool, remark: str):
        asyncio.create_task(
            get_bots()[str(self.bot_info.id)].set_friend_add_request(
                flag=flag, approve=approve, remark=remark
            )
        )

    def set_group_add_request(
        self, flag: str, sub_type: str, approve: bool, remark: str
    ):
        asyncio.create_task(
            get_bots()[str(self.bot_info.id)].set_group_add_leave(
                flag=flag, sub_type=sub_type, approve=approve, remark=remark
            )
        )

    def reply(self, message: str):
        if self.data:
            asyncio.create_task(
                get_bots()[str(self.bot_info.id)].send(self.data, Message(message))
            )
