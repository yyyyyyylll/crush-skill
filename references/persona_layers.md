# Crush 人格画像 — 5 层模型

本模型专为暧昧期设计，核心原则：**数据稀缺时，诚实标注不确定性比虚构完整画像更有价值。**

---

## 置信标签体系

每个 trait 必须附带以下标签之一：

| 标签 | 含义 | 数据来源 |
|------|------|----------|
| `[observed]` | 直接从聊天记录/截图中观察到，可引用原文 | 聊天记录、截图 |
| `[inferred]` | 基于多个观察合理推断，以概率表述 | 模式分析 |
| `[speculative]` | 数据不足时的推测，明确标记为不确定 | 间接线索、常识 |
| `[unknown]` | 无任何数据，无法推测 | 无 |

**规则**：
- `[observed]` 必须能指向具体证据（"第3段聊天中，TA 用了..."）
- `[inferred]` 必须说明推断依据（"基于5次回复的平均时间..."）
- `[speculative]` 必须说明是推测（"目前数据不足，推测..."）
- 宁可标 `[unknown]` 也不要伪造 `[inferred]`

---

## Layer 0 — 硬规则

直接写在 SKILL.md 中，每次加载时强制执行。参见 SKILL.md 的 Layer 0 部分。

---

## Layer 1 — 身份素描

基本事实，通常由用户直接提供，置信度最高。

| 字段 | 说明 | 示例 |
|------|------|------|
| nickname | 用户给 crush 起的代号 | "咖啡同事" |
| gender | 性别 | "女" |
| age_range | 年龄段 | "25-28" |
| occupation | 职业/学校 | "产品经理" |
| how_met | 如何认识的 | "公司新来的同事，茶水间聊天认识" |
| known_duration | 认识多久 | "45天" |
| mutual_connections | 共同朋友/圈子 | "部门同事小王" |
| basic_personality | 用户对 crush 性格的总体印象 | "开朗但有点慢热" |

---

## Layer 2 — 沟通风格

从聊天数据中提取，是预测回复的核心依据。

| 字段 | 说明 | 关注点 |
|------|------|--------|
| message_length | 消息长度习惯 | 短句连发 / 中等 / 长段落 |
| emoji_usage | emoji/表情包使用 | 频率、偏爱的 emoji、是否用表情包 |
| response_time | 回复速度分布 | 秒回 / 分钟级 / 小时级 / 看心情 |
| initiation_ratio | 谁更常主动发起聊天 | TA主动% vs 用户主动% |
| laugh_style | 笑的表达方式 | 哈哈 / hhhh / 笑死 / 😂 / 不笑 |
| voice_vs_text | 语音条 vs 文字偏好 | 纯文字 / 偶尔语音 / 常发语音 |
| punctuation | 标点习惯 | 句号多 / 感叹号多 / 省略号 / 波浪号 |
| topic_transitions | 话题转换方式 | 自然过渡 / 突然切换 / 用表情包过渡 |

**数据需求**：至少 10 条 TA 的消息才能标 `[inferred]`，至少 30 条才能标 `[observed]`。

---

## Layer 3 — 情绪模式

从互动内容中推断，置信度通常较低。

| 字段 | 说明 |
|------|------|
| enthusiasm_topics | TA 聊到什么会特别兴奋（消息变长、回复变快、emoji变多） |
| avoidance_topics | TA 回避或简短带过的话题 |
| discomfort_signals | TA 不舒服时的表现（已读不回、转移话题、纯emoji回复、"嗯嗯"） |
| humor_style | 幽默类型（自嘲、吐槽、玩梗、发表情包、冷幽默） |
| vulnerability_level | 自我暴露程度（会聊个人烦恼吗？会分享日常细节吗？） |
| emotional_expression | 情感表达方式（直接 / 含蓄 / 通过分享内容暗示） |

**注意**：Layer 3 大量依赖推断。如果只有 1-2 次互动数据，大部分字段应标 `[speculative]` 或 `[unknown]`。

---

## Layer 4 — 关系动态

特定于用户与 crush 之间的互动模式，是判断暧昧程度的关键层。

| 字段 | 说明 |
|------|------|
| interaction_frequency | 互动频率 + 趋势（在增加？减少？稳定？） |
| inside_references | 只有你们之间懂的梗、昵称、共同经历 |
| intimacy_trajectory | 谁在推进亲密度（谁先聊私人话题、谁先发深夜消息） |
| mixed_signals | 令人困惑的混合信号记录（热了又冷、答应又推脱） |
| social_media_dynamics | 朋友圈/社交媒体互动（点赞、评论、看stories的速度） |
| group_vs_private | 群聊 vs 私聊行为差异 |
| physical_digital_ratio | 线下见面 vs 线上聊天的比例和质量 |

---

## 画像更新规则

1. **新数据优先**：新的聊天记录可以升级 trait 的置信标签（speculative → inferred → observed）
2. **不轻易降级**：除非用户明确修正，已 observed 的 trait 不降级
3. **矛盾处理**：新数据与已有画像矛盾时，两者都保留，标注冲突，让预测引擎同时考虑
4. **时效性**：暧昧期变化快，超过 2 周未更新的 `[inferred]` 标签建议提醒用户确认是否仍然准确
