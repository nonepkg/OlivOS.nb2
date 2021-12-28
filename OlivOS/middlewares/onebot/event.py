from typing import Callable, Dict, Optional, Type

from nonebot import get_bot
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import *
from nonebot.adapters.cqhttp.message import Message

from OlivOS.middlewares import ID, MSG, BotInfo
from OlivOS.middlewares import OlivOSEvent as BaseOlivOSEvent
from OlivOS.middlewares import Result


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
            self.data.sender["name"] = event.sender.nickname
            self.data.sender["id"] = event.sender.user_id
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

    def reply(self, message: MSG):
        if self.data:
            self.run_async(
                get_bot(str(self.bot_info.id)).send(self.data, Message(message))
            )

    def send(self, send_type: str, target_id: ID, message: MSG):
        self.call_api(
            "send_msg",
            message_type=send_type,
            user_id=int(target_id) if send_type == "private" else None,
            group_id=int(target_id) if send_type == "group" else None,
            message=Message(message),
        )

    def delete_msg(self, message_id: ID):
        self.call_api("delete_msg", message_id=int(message_id))

    def get_msg(self, message_id: ID) -> Result:
        return self.call_api("get_msg", message_id=int(message_id))

    def send_like(self, user_id: ID):
        self.call_api("like", user_id=int(user_id))

    def set_group_kick(self, group_id: ID, user_id: ID):
        self.call_api("set_group_kick", group_id=int(group_id), user_id=int(user_id))

    def set_group_ban(self, group_id: ID, user_id: ID):
        self.call_api("set_group_ban", group_id=int(group_id), user_id=int(user_id))

    def set_group_whole_ban(self, group_id: ID, enable):
        self.call_api("set_group_whole_ban", group_id=int(group_id), enable=enable)

    def set_group_admin(self, group_id: ID, user_id: ID, enable: bool):
        self.call_api(
            "set_group_admin",
            group_id=int(group_id),
            user_id=int(user_id),
            enable=enable,
        )

    def set_group_card(self, group_id: ID, user_id: ID, card: str):
        self.call_api(
            "set_group_card", group_id=int(group_id), user_id=int(user_id), card=card
        )

    def set_group_name(self, group_id: ID, group_name: str):
        self.call_api("set_group_name", group_id=int(group_id), group_name=group_name)

    def set_group_leave(self, group_id: ID):
        self.call_api("set_group_leave", group_id=int(group_id))

    def set_group_special_title(
        self, group_id: ID, user_id: ID, special_title: str, duration: int
    ):
        self.call_api(
            "set_group_special_title",
            group_id=int(group_id),
            user_id=int(user_id),
            special_title=special_title,
            duration=duration,
        )

    def set_friend_add_request(self, flag: ID, approve: bool, remark: str):
        self.call_api(
            "set_friend_add_request",
            flag=str(flag),
            approve=approve,
            remark=remark,
        )

    def set_group_add_request(
        self, flag: ID, sub_type: str, approve: bool, reason: str
    ):
        self.call_api(
            "set_group_add_request",
            flag=str(flag),
            sub_type=sub_type,
            approve=approve,
            reason=reason,
        )

    def get_login_info(self):
        return self.call_api("get_login_info")

    def get_stranger_info(self, user_id: ID):
        return self.call_api("get_stranger_info", user_id=int(user_id))

    def get_friend_list(self):
        return self.call_api("get_friend_list")

    def get_group_info(self):
        return self.call_api("get_group_info")

    def get_group_list(self):
        return self.call_api("get_group_list")

    def get_group_member_info(self):
        return self.call_api("get_group_member_info")

    def get_group_member_list(self):
        return self.call_api("get_group_member_list")
