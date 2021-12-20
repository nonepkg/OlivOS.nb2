import hashlib

from nonebot import get_bots
from nonebot.adapters import Bot
from nonebot.log import logger


class BotInfo:
    def __init__(self, id: int, platform: dict) -> None:
        self.id = id
        self.platform = platform
        self.hash = self.get_hash()

    def get_hash(self):
        hash_tmp = hashlib.new("md5")
        hash_tmp.update(str(self.id).encode(encoding="UTF-8"))
        hash_tmp.update(str(self.platform["sdk"]).encode(encoding="UTF-8"))
        hash_tmp.update(str(self.platform["platform"]).encode(encoding="UTF-8"))
        # hash_tmp.update(str(platform_model).encode(encoding='UTF-8'))
        return hash_tmp.hexdigest()


class Proc:
    def __init__(self) -> None:
        self.Proc_data = {}
        self.Proc_data["bot_info_dict"] = {}
        for bot in get_bots().values():
            if isinstance(bot, Bot):
                bot_info = BotInfo(
                    int(bot.self_id),
                    {"sdk": "onebot", "platform": "qq", "model": "nonebot"},
                )
                self.Proc_data["bot_info_dict"].update({bot_info.hash: bot_info})
        self.log = lambda log_level, log_message, log_segment: logger.info(log_message)
