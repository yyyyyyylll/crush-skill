<h1 align="center">暧昧.skill</h1>

<p align="center"><b>TA 回消息了吗？没有。那如果我发这条呢？</b></p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.9%2B-blue.svg" alt="Python 3.9+"></a>
  <a href="https://claude.ai/code"><img src="https://img.shields.io/badge/Claude%20Code-Skill-blueviolet" alt="Claude Code"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/AgentSkills-Standard-green" alt="AgentSkills"></a>
</p>

<p align="center">
你编辑了一条消息又删掉了？<br>
你截图发给朋友问"这样回是不是有意思"？<br>
你盯着"对方正在输入..."心跳加速结果等来一个"哈哈"？<br>
你半夜翻聊天记录试图从 emoji 里读出爱情？<br>
你想约 TA 出来但那条消息在输入框里躺了三天？<br>
<br>
<b>把暧昧期的忐忑交给 AI，发送前先彩排一遍。</b>
</p>

<p align="center">
提供 crush 的聊天记录、社交媒体、你的描述<br>
生成一个 <b>TA 的沟通画像</b><br>
预测 TA 怎么回你的消息，或者直接扮演 TA 跟你聊天
</p>

<p align="center">⚠️ <b>本项目仅用于个人情感辅助，不用于骚扰、跟踪或操纵他人。TA 是一个真实的人，不是攻略对象。</b></p>

<p align="center">
  <a href="#安装">安装</a> · <a href="#使用">使用</a> · <a href="#效果示例">效果示例</a>
</p>

---

### 🌟 同系列项目

> 暧昧是爱情的序章，前任是爱情的番外。<br>
> 用 **crush.skill** 把 TA 追到手，万一有天散了，还有 **[前任.skill](https://github.com/therealXiaomanChu/ex-skill)** 帮你留住那些回忆。<br>
> 先追到，再追忆 —— 希望你永远只需要第一个 💛

---

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/yyyyyyylll/crush-skill .claude/skills/crush

# 或安装到全局（所有项目都能用）
git clone https://github.com/yyyyyyylll/crush-skill ~/.claude/skills/crush
```

### OpenClaw

```bash
git clone https://github.com/yyyyyyylll/crush-skill ~/.openclaw/workspace/skills/crush
```

### 依赖（可选）

```bash
pip3 install -r requirements.txt
```

---

## 使用

在 Claude Code 中输入：

```
/crush
```

按提示给 crush 起个代号，描述基本信息和互动情况，然后提供聊天记录。所有字段均可跳过，仅凭描述也能生成。

完成后可以预测消息、模拟对话、解读信号、看温度计。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/crush` | 创建新的 crush 档案 |
| `/list-crushes` | 列出所有 crush 档案 |
| `/{slug}` | 进入模拟对话（像 TA 一样跟你聊天） |
| `/{slug}-predict` | 预测模式（发消息前看看 TA 会怎么回） |
| `/{slug}-signals` | 信号解读（分析最近互动） |
| `/{slug}-temp` | 暧昧温度计 |
| `/crush-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-crush {slug}` | 删除档案 |
| `/move-on {slug}` | 释然（delete 的温柔别名）|

---

## 效果示例

> 输入：`公司新来的同事，产品经理，开朗但有点慢热，认识一个半月，每天都聊，爱发😂和表情包`

**场景一：模拟对话**

```
用户      ❯ 今天好累啊

暧昧.skill ❯ 怎么了 加班了？😂

用户      ❯ 嗯 搞到九点多

暧昧.skill ❯ 也太惨了吧哈哈哈哈 吃饭了没
```

**场景二：预测回复**

```
用户      ❯ 我想发这条消息："周末有空吗？想去看那个展"

暧昧.skill ❯ ═══ 消息预测 ═══

             📱 最可能 (~55%): "可以呀！几点？"
             ⏱ 5-15分钟 | 🌡 热情度 8/10
             💭 对见面有兴趣，回复干脆说明没犹豫

             📱 备选 (~25%): "周末可能有点事，看看时间再说？"
             ⏱ 30分钟-1小时 | 🌡 热情度 5/10

             📱 冷回复 (~15%): "那个展好像还行"
             ⏱ 1-3小时 | 🌡 热情度 3/10

             ⚠️ 置信度: 60% | 基于 3 周聊天记录
```

**场景三：信号解读**

```
用户      ❯ 帮我分析一下最近这几天的聊天

暧昧.skill ❯ ═══ 信号解读报告 ═══

             📊 综合判断: 偏暖 (65% 积极信号)

             ✅ 积极信号
             • [observed] 最近 3 次聊天 TA 发起了 2 次
             • [observed] 开始主动分享日常（发了周末出去玩的照片）
             • [inferred] 回复速度比上周快了

             ❓ 模糊信号
             • 拒绝了周末见面但给了理由——可能真的有事，也可能在回避
```

**场景四：暧昧温度计**

```
用户      ❯ 看温度计

暧昧.skill ❯ ═══ 暧昧温度计 ═══

               冷漠 | 礼貌 | 友好 | 暧昧 | 明确
               0-20 | 20-40| 40-60| 60-80| 80-100
                                      ▲
                                 当前: 68° [上周: 62°]

             📈 趋势: 缓慢上升 (+6°/周)
             ⚠️ 误差范围: ±12°
```

---

## 功能特性

### 两大模式

本 skill 提供两种核心体验，随时切换：

| | 模拟模式 | 分析模式 |
|---|---|---|
| **身份** | AI 扮演 crush | 分析助手 |
| **输出** | 直接回复（像 TA 会说的话） | 报告、概率、置信度 |
| **用途** | 找感觉、彩排对话 | 理性决策、信号判断 |
| **切换** | 说"退出模拟" 或 `/{slug}-predict` 等 → 分析模式 | 说"和 TA 聊聊" 或 `/{slug}` → 模拟模式 |

切换支持两种方式，随你习惯：

- **自然语言**：直接说"和 TA 聊聊"、"退出模拟"、"这句话真发会怎样"，AI 自动识别意图并切换
- **Slash 命令**：`/{slug}` 进模拟，`/{slug}-predict` 预测回复，`/{slug}-signals` 信号解读，`/{slug}-temp` 温度计，`/{slug}-strategy` 策略建议

### 数据源

| 来源 | 格式 | 备注 |
|------|------|------|
| 微信聊天记录 | WeChatMsg / 留痕 / PyWxDump 导出 | 推荐，信息最丰富 |
| 聊天截图 | PNG / JPG | 自动识别消息内容 |
| 朋友圈/微博/小红书 | 截图或文本 | 提取兴趣和社交风格 |
| 口述/粘贴 | 纯文本 | 你的主观描述 |

### 生成的画像结构

每个 crush 画像由 5 层组成，每个字段带置信标签：

| 层 | 内容 | 置信度来源 |
|---|---|---|
| **Layer 0 — 硬规则** | 不骚扰、标注不确定性、尊重真人 | 固定 |
| **Layer 1 — 身份素描** | 昵称、年龄、职业、认识方式 | 用户描述 `[observed]` |
| **Layer 2 — 沟通风格** | 消息长度、emoji、回复速度、笑法 | 聊天记录 `[observed/inferred]` |
| **Layer 3 — 情绪模式** | 热衷话题、回避话题、幽默风格 | 推断 `[inferred/speculative]` |
| **Layer 4 — 关系动态** | 互动频率、内部梗、混合信号 | 混合 `[variable]` |

运行逻辑：`收到消息 → 画像判断 TA 会怎么回 → 用 TA 的风格输出（模拟）/ 生成概率报告（分析）`

### 置信标签体系

暧昧期数据有限，诚实比完整更重要：

| 标签 | 含义 |
|------|------|
| `[observed]` | 直接从聊天记录中观察到，可引用原文 |
| `[inferred]` | 基于多个观察合理推断 |
| `[speculative]` | 数据不足时的推测，明确标记 |
| `[unknown]` | 无数据，不编造 |

### 进化机制

- **补充数据** → 找到更多聊天记录 → 自动分析增量 → 画像精度提升
- **预测修正** → 说「TA 实际回了 xxx」→ 对比偏差 → 更新画像层
- **版本管理** → 每次更新自动存档，支持回滚

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准：

```
crush-skill/
├── SKILL.md                  # skill 入口（官方 frontmatter）
├── prompts/                  # Prompt 模板
│   ├── intake.md             #   对话式信息录入
│   ├── persona_builder.md    #   5 层画像构建
│   ├── message_predictor.md  #   消息预测引擎
│   ├── simulator.md          #   模拟对话模式
│   ├── signal_reader.md      #   信号解读
│   ├── thermometer.md        #   暧昧温度计
│   ├── correction_handler.md #   预测修正处理
│   └── strategy_advisor.md   #   消息策略建议
├── tools/                    # Python 工具
│   ├── wechat_parser.py      #   微信聊天记录解析
│   ├── social_media_parser.py #  社交媒体解析
│   └── profile_manager.py    #   档案管理与版本控制
├── references/               # 参考资料
│   ├── persona_layers.md     #   5 层人格模型定义
│   ├── signal_taxonomy.md    #   信号分类表（积极/消极/模糊）
│   ├── response_patterns.md  #   暧昧期回复模式库
│   └── screenshot_guide.md   #   聊天截图分析指引
├── examples/                 # 示例
│   └── example_profile.json  #   示例 crush 档案
└── LICENSE
```

---

## 注意事项

- **聊天记录质量决定预测精度**：有记录 > 仅描述，30 条以上效果明显提升
- 建议优先提供：**深夜聊天** > **邀约相关对话** > **日常消息**（最能体现真实态度）
- 本项目不鼓励对暧昧对象的不健康执念，如果你发现自己反复纠结同一条消息，先放下手机
- TA 是一个真实的人，有自己的生活和选择。这个 Skill 只是帮你理清思路，不是替你决定

### 推荐的聊天记录导出工具

以下工具为独立的开源项目，本项目不包含它们的代码，仅在解析器中适配了它们的导出格式：

- **[WeChatMsg](https://github.com/LC044/WeChatMsg)** — 微信聊天记录导出（Windows）
- **[PyWxDump](https://github.com/xaoyaoo/PyWxDump)** — 微信数据库解密导出（Windows）
- **留痕** — 微信聊天记录导出（macOS）

---

## 致敬 & 引用

本项目的架构灵感来源于 **[同事.skill](https://github.com/titanwings/colleague-skill)**（by [titanwings](https://github.com/titanwings)）和 **[前任.skill](https://github.com/therealXiaomanChu/ex-skill)**（by [therealXiaomanChu](https://github.com/therealXiaomanChu)）。

同事.skill 首创了"把人蒸馏成 AI Skill"的双层架构，前任.skill 将其迁移到了恋爱场景，暧昧.skill 在此基础上聚焦暧昧期的不确定性预测。致敬两位原作者的创意和开源精神。

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准，兼容 Claude Code 和 OpenClaw。

---

### 写在最后

暧昧期最大的陷阱，是你开始表演一个更容易被喜欢的自己。

你揣摩 TA 想听什么，你计算回复的最佳时间，你在每条消息里埋伏笔。你以为这是策略，其实是恐惧——怕真实的自己不够好。

这个 Skill 能帮你分析信号、预测回复、模拟对话。但它最大的价值不是教你怎么"套路" TA，而是帮你看清局势之后，给你勇气做自己。

真诚，是永远的必杀技。

用数据看清方向，然后把攻略放下，用你自己的话，去说你真正想说的。

---

<div align="center">

MIT License

</div>
