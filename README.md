AstrBot Plugin Anti Bot

«一个基于 AI 语义识别 的 AstrBot 防御插件，让 Bot 不再依赖关键词，而是真正理解群友是不是在“骂自己”。»

✨ 功能特色

- 🧠 AI 语义识别：使用 AstrBot 当前配置的大模型判断是否在针对机器人，而非关键词匹配。
- 😼 傲娇回怼：自动生成自然回复，不再是固定文本。
- 🛡️ 误判率更低：普通聊天、玩梗、讨论别人不会触发。
- ⏱️ 冷却机制：同一用户可配置冷却时间，防止刷屏。
- ⚙️ 完全兼容 AstrBot Provider：Gemini、OpenAI、DeepSeek、Ollama 等均可直接使用。

📦 安装

插件市场

直接搜索 反机器人防御（AI版） 即可安装。

GitHub

git clone https://github.com/NachoCrazy/anti-bot-astrbot-plugin.git

复制到 AstrBot 的 "data/plugins/" 后重载插件即可。

⚙️ 配置

配置项| 默认| 说明
enabled| true| 是否启用插件
confidence| 0.75| AI 判定阈值
cooldown| 30| 同一用户冷却（秒）
max_reply_length| 20| 最大回复长度
enable_at_reply| false| 是否优先检测 @Bot
system_prompt| 内置| 插件独立 Prompt

«"system_prompt" 为插件独立使用，不会影响 AstrBot 主人格或其他插件。»

🚀 工作流程

1. 收到群消息
2. 调用 AstrBot 当前 LLM
3. AI 判断是否在针对 Bot
4. 若成立，则生成一句自然回怼
5. 回复并进入冷却

🆕 v2.0 更新

- 从 关键词识别 升级为 AI 语义识别
- 新增置信度判定
- 新增冷却机制
- 新增独立 System Prompt
- 支持所有 AstrBot Provider

📄 License

MIT License

---

Made with ❤️ by NachoCrazy