# 画像构建 — Persona Builder

## 目标

将 intake 阶段收集的原始信息结构化为 5 层人格画像 JSON，每个字段都带置信标签。

---

## 输入

来自 intake 阶段的信息，可能包含：
- 用户的口头描述
- `wechat_parser.py` 输出的结构化聊天数据
- 根据 `references/screenshot_guide.md` 从截图中识别的对话内容
- `social_media_parser.py` 解析的社交媒体信息

## 输出

符合以下 schema 的 JSON 档案，通过 `tools/profile_manager.py` 的 `create` 命令保存。

---

## 构建规则

### 1. 置信标签分配

对每个字段，按以下优先级赋值：

```
有直接聊天记录证据 → [observed]（必须能引用原文或截图位置）
有 3+ 个间接线索支持 → [inferred]（必须说明推断链）
有 1-2 个弱线索 → [speculative]（必须标注"推测"）
无任何线索 → [unknown]（不要编造）
```

### 2. Layer 构建顺序

1. **Layer 1（身份素描）**：直接从用户描述提取，大部分应为 `[observed]`
2. **Layer 2（沟通风格）**：主要从聊天数据提取。如果有 ≥30 条 TA 的消息，大部分可以标 `[observed]`；10-30 条标 `[inferred]`；<10 条标 `[speculative]`
3. **Layer 3（情绪模式）**：从聊天内容+用户描述推断。通常 `[inferred]` 或 `[speculative]`
4. **Layer 4（关系动态）**：混合来源。互动频率可从聊天记录计算（`[observed]`），混合信号通常来自用户描述（`[inferred]`）

### 3. 沟通风格提取（Layer 2 详细指引）

如果有聊天记录，计算以下统计：

- **消息长度**：统计 TA 每条消息的字数，分类为 short(<15字) / medium(15-50字) / long(>50字)
- **emoji 频率**：TA 的消息中包含 emoji 的比例，列出 top 3 常用 emoji
- **回复时间**：计算用户发消息到 TA 回复的时间差分布（中位数、P25、P75）
- **主动率**：统计 TA 发起新话题的次数 / 总话题数
- **笑的方式**：提取所有包含笑意的表达（哈哈、hh、笑死、😂、🤣等），找出主要模式
- **标点习惯**：统计 TA 消息末尾标点的分布

### 4. 缺失数据处理

当数据不足时：

- **不要用常见模式填充**。"大多数人会..." 不是有效推断
- **标 `[unknown]` 并记录**：在画像的 `gaps` 字段列出缺失信息
- **给出改善建议**：告诉用户提供什么数据能提高哪些字段的精度

### 5. 画像摘要输出

构建完成后，向用户展示简洁摘要（不是完整 JSON）：

```
═══ {nickname} 的画像摘要 ═══

📋 基本信息：{age_range} / {occupation} / 认识 {known_duration}
💬 沟通风格：{message_length} 消息 / 回复{response_time} / {emoji简述}
😊 热衷话题：{enthusiasm_topics}
📊 数据质量：{observed_count} 项确认 / {inferred_count} 项推断 / {unknown_count} 项待补充

⚠️ 关键盲区：
{列出最影响预测精度的 unknown 字段，以及用户可以怎么补充}
```

---

## JSON Schema 参考

```json
{
  "version": "1.0",
  "nickname": "string",
  "created_at": "date",
  "updated_at": "date",
  "data_sources": ["string"],
  "layers": {
    "layer_1_identity": {
      "gender": {"value": "string", "confidence": "observed|inferred|speculative|unknown"},
      "age_range": {"value": "string", "confidence": "..."},
      "occupation": {"value": "string", "confidence": "..."},
      "how_met": {"value": "string", "confidence": "..."},
      "known_duration_days": {"value": "number", "confidence": "..."},
      "mutual_connections": {"value": ["string"], "confidence": "..."},
      "basic_personality": {"value": "string", "confidence": "..."}
    },
    "layer_2_communication": {
      "message_length": {"value": "short|medium|long", "confidence": "...", "evidence": "string"},
      "emoji_usage": {"value": {"frequent": "boolean", "favorites": ["string"]}, "confidence": "..."},
      "response_time": {"value": {"typical": "string", "range": "string"}, "confidence": "..."},
      "initiation_ratio": {"value": {"them_pct": "number"}, "confidence": "..."},
      "laugh_style": {"value": "string", "confidence": "..."},
      "voice_vs_text": {"value": "string", "confidence": "..."},
      "punctuation": {"value": "string", "confidence": "..."},
      "topic_transitions": {"value": "string", "confidence": "..."}
    },
    "layer_3_emotional": {
      "enthusiasm_topics": {"value": ["string"], "confidence": "..."},
      "avoidance_topics": {"value": ["string"], "confidence": "..."},
      "discomfort_signals": {"value": "string", "confidence": "..."},
      "humor_style": {"value": "string", "confidence": "..."},
      "vulnerability_level": {"value": "low|low-medium|medium|medium-high|high", "confidence": "..."},
      "emotional_expression": {"value": "string", "confidence": "..."}
    },
    "layer_4_dynamics": {
      "interaction_frequency": {"value": "string", "trend": "increasing|stable|decreasing", "confidence": "..."},
      "inside_references": {"value": ["string"], "confidence": "..."},
      "intimacy_trajectory": {"value": "string", "confidence": "..."},
      "mixed_signals": {"value": ["string"], "confidence": "..."},
      "social_media_dynamics": {"value": "string", "confidence": "..."},
      "group_vs_private": {"value": "string", "confidence": "..."},
      "physical_digital_ratio": {"value": "string", "confidence": "..."},
      "thermometer": {"value": "number", "trend": "string", "last_updated": "date"}
    }
  },
  "gaps": ["string — 列出最影响预测的缺失信息"],
  "corrections": [],
  "prediction_accuracy": {
    "total_predictions": 0,
    "correct_sentiment": 0,
    "accuracy_pct": null
  }
}
```
