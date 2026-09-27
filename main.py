import json
import time

from astrbot.api.star import Context, Star, register
from astrbot.api.event import AstrMessageEvent, filter

SYSTEM_PROMPT = """
你是QQ群机器人防御检测器。

任务：
判断用户是否在辱骂、嘲讽、挑衅机器人本人。

规则：
1. 对象必须是机器人/Bot/AI。
2. 普通聊天、玩梗、讨论别人，一律 attack=false。
3. 如果攻击成立，生成一句20字以内的傲娇回怼。
4. 禁止脏话、政治、辱骂家人。

只输出 JSON：

攻击：
{"attack":true,"reply":"哈？你先学会用再说！"}

未攻击：
{"attack":false}
"""

@register(
    "astrbot_plugin_anti_bot",
    "NachoCrazy",
    "AI语义防御插件",
    "2.0.0",
)
class AntiBotPlugin(Star):

    def __init__(self, context: Context):
        super().__init__(context)
        self.cooldown = {}

    @filter.event_message_type(filter.EventMessageType.GROUP_MESSAGE)
    async def on_group(self, event: AstrMessageEvent):

        # 不处理自己
        if event.get_sender_id() == event.get_self_id():
            return

        uid = str(event.get_sender_id())
        now = time.time()

        # 30 秒冷却
        if uid in self.cooldown and now - self.cooldown[uid] < 30:
            return

        provider = self.context.get_using_provider()

        result = await provider.text_chat(
            prompt=event.message_str,
            system_prompt=SYSTEM_PROMPT,
            temperature=0.2,
            max_tokens=80,
        )

        text = (
            result.completion_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            data = json.loads(text)
        except Exception:
            return

        if not data.get("attack", False):
            return

        self.cooldown[uid] = now

        yield event.plain_result(data["reply"])