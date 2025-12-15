henghetonguol# main.py —— 终极 NapCat 兼容版
from astrbot.api import star
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.core.message.message_event_result import MessageChain
from astrbot.api import AstrBotConfig, logger
import random

# 默认配置常量
DEFAULT_NEGATIVE_KEYWORDS = ["机器人", "bot", "人机"]
DEFAULT_POSITIVE_KEYWORDS = ["好", "棒", "赞", "优秀", "聪明"]
DEFAULT_REPLY = "你才是机器人baka！！！😡"
DEFAULT_AT_REPLY = "你@我干嘛！有种再说一遍？你才是机器人baka！！！💢"
DEFAULT_TEST_REPLY = "test你妈喵 🤬"

class Main(star.Star):
    def __init__(self, context: star.Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @filter.regex(r"(?i)(机器人|bot|人机)", priority=9)
    async def anti_bot(self, event: AstrMessageEvent):
        enabled = self.config.get("enabled", True)
        if not enabled:
            return

        # 获取负面关键词和正面关键词
        negative_keywords = self.config.get("negative_keywords", DEFAULT_NEGATIVE_KEYWORDS)
        positive_keywords = self.config.get("positive_keywords", DEFAULT_POSITIVE_KEYWORDS)
        
        # 检查是否包含负面关键词
        message = event.message_str.lower()
        contains_negative = any(keyword.lower() in message for keyword in negative_keywords)
        
        # 检查是否包含正面关键词
        contains_positive = any(keyword.lower() in message for keyword in positive_keywords)
        
        # 只有包含负面关键词且不包含正面关键词时才触发
        if not contains_negative or contains_positive:
            return

        # 防自触发（优化：检查是否包含自己的回复关键词）
        if any(word in event.message_str.lower() for word in ["baka", "你才是"]):
            return

        reply = self.config.get("reply_text", DEFAULT_REPLY)
        at_reply = self.config.get("at_reply_text", DEFAULT_AT_REPLY)

        # 检测是否被@
        is_at_me = event.is_at_or_wake_command
        
        # 记录调试信息
        logger.debug(f"Anti-bot triggered: message='{event.message_str}', is_at_me={is_at_me}, is_at_or_wake_command={event.is_at_or_wake_command}")

        final_reply = at_reply if is_at_me else reply

        if self.config.get("add_emoji", True):
            angry_emojis = ["💢", "😤", "🤬", "🔥", "👊", "💥"]
            final_reply += random.choice(angry_emojis)

        await event.send(MessageChain().message(final_reply))

    @filter.regex(r"(?i)(test|测试)", priority=8)
    async def anti_test(self, event: AstrMessageEvent):
        """检测到test或测试关键词时的特殊回复"""
        enabled = self.config.get("enabled", True)
        if not enabled:
            return
            
        # 防自触发
        if "test你妈喵" in event.message_str:
            return
            
        test_reply = self.config.get("test_reply_text", DEFAULT_TEST_REPLY)
        await event.send(MessageChain().message(test_reply))