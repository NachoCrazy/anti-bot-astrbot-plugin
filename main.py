# main.py —— 终极 NapCat 兼容版
from astrbot.api import star
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.core.message.message_event_result import MessageChain
from astrbot.api import AstrBotConfig
import re
import random

class Main(star.Star):
    def __init__(self, context: star.Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @filter.regex("", priority=9)
    async def anti_bot(self, event: AstrMessageEvent):
        enabled = self.config.get("enabled", True)
        if not enabled:
            return

        detect_regex = self.config.get("detect_regex",
            r"(?i).*(bot|机器人|机机人|你是[个個]?机器|bot.?bot|机器人.?机器人).*"
        )

        if not re.search(detect_regex, event.message_str):
            return

        # 防自触发（优化：检查是否包含自己的回复关键词）
        if any(word in event.message_str.lower() for word in ["baka", "你才是"]):
            return

        reply = self.config.get("reply_text", "你才是机器人baka！！！😡")
        at_reply = self.config.get("at_reply_text", "你@我干嘛！有种再说一遍？你才是机器人baka！！！💢")

        # 正确获取 bot ID：从底层消息对象取（NapCat/OneBot 兼容）
        bot_id = event.message_obj.self_id if hasattr(event.message_obj, 'self_id') else "0"

        # NapCat 被@检测：[CQ:at,qq=BOT_ID]
        is_at_me = f"[CQ:at,qq={bot_id}]" in event.message_str
        final_reply = at_reply if is_at_me else reply

        if self.config.get("add_emoji", True):
            angry_emojis = ["💢", "😤", "🤬", "🔥", "👊", "💥"]
            final_reply += random.choice(angry_emojis)

        await event.send(MessageChain().message(final_reply))