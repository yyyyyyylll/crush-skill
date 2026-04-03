#!/usr/bin/env python3
"""
微信聊天记录解析器

支持格式:
1. 微信桌面端导出的 .txt 文件
2. 手动复制粘贴的聊天文本

输出: 结构化 JSON，包含消息列表和统计数据。

用法:
    python wechat_parser.py <file_path> <crush_name>
    python wechat_parser.py --stdin <crush_name>  # 从标准输入读取
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path


# 微信桌面端导出格式: "2024-03-15 14:30:22 昵称"
WECHAT_DESKTOP_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+)$"
)

# 微信手机端复制格式: "昵称 2024/3/15 14:30" 或 "昵称 14:30"
WECHAT_MOBILE_PATTERN = re.compile(
    r"^(.+?)\s+(\d{4}/\d{1,2}/\d{1,2}\s+\d{1,2}:\d{2}|\d{1,2}:\d{2})$"
)

# 通用时间戳格式
GENERIC_TIMESTAMP_PATTERN = re.compile(
    r"^[\[【]?(\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}(?::\d{2})?)[\]】]?\s*(.+)$"
)

EMOJI_PATTERN = re.compile(
    r"[\U0001F600-\U0001F64F"  # emoticons
    r"\U0001F300-\U0001F5FF"   # symbols & pictographs
    r"\U0001F680-\U0001F6FF"   # transport & map
    r"\U0001F1E0-\U0001F1FF"   # flags
    r"\U00002702-\U000027B0"
    r"\U0000FE00-\U0000FE0F"
    r"\U0001F900-\U0001F9FF"   # supplemental
    r"\U0001FA00-\U0001FA6F"   # chess symbols
    r"\U0001FA70-\U0001FAFF"   # symbols extended
    r"\U00002600-\U000026FF"   # misc symbols
    r"]+",
    flags=re.UNICODE,
)


def parse_timestamp(ts_str: str) -> datetime | None:
    """尝试解析各种时间戳格式"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%H:%M",  # 手机端时间（无日期）
    ]
    for fmt in formats:
        try:
            return datetime.strptime(ts_str.strip(), fmt)
        except ValueError:
            continue
    return None


def parse_messages(text: str, crush_name: str) -> list[dict]:
    """解析聊天文本为消息列表"""
    messages = []
    current_msg = None
    lines = text.strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 尝试匹配各种格式的消息头
        parsed = None

        # 格式1: 桌面端 "2024-03-15 14:30:22 昵称"
        m = WECHAT_DESKTOP_PATTERN.match(line)
        if m:
            parsed = {"timestamp": m.group(1), "sender": m.group(2).strip()}

        # 格式2: 手机端复制 "昵称 2024/3/15 14:30"
        if not parsed:
            m = WECHAT_MOBILE_PATTERN.match(line)
            if m:
                parsed = {"timestamp": m.group(2), "sender": m.group(1).strip()}

        # 格式3: 通用时间戳
        if not parsed:
            m = GENERIC_TIMESTAMP_PATTERN.match(line)
            if m:
                parsed = {"timestamp": m.group(1), "sender": m.group(2).strip()}

        if parsed:
            # 保存上一条消息
            if current_msg and current_msg.get("content"):
                messages.append(current_msg)

            ts = parse_timestamp(parsed["timestamp"])
            current_msg = {
                "sender": parsed["sender"],
                "timestamp": parsed["timestamp"],
                "datetime": ts.isoformat() if ts else None,
                "content": "",
                "is_crush": crush_name.lower() in parsed["sender"].lower(),
            }
        elif current_msg is not None:
            # 多行消息的后续行
            if current_msg["content"]:
                current_msg["content"] += "\n"
            current_msg["content"] += line
        else:
            # 可能是没有时间戳的格式，尝试按 "昵称: 内容" 解析
            colon_match = re.match(r"^(.+?)[：:]\s*(.+)$", line)
            if colon_match:
                sender = colon_match.group(1).strip()
                content = colon_match.group(2).strip()
                messages.append({
                    "sender": sender,
                    "timestamp": None,
                    "datetime": None,
                    "content": content,
                    "is_crush": crush_name.lower() in sender.lower(),
                })

    # 保存最后一条消息
    if current_msg and current_msg.get("content"):
        messages.append(current_msg)

    return messages


def compute_statistics(messages: list[dict], crush_name: str) -> dict:
    """计算聊天统计数据，用于构建 Layer 2"""

    crush_msgs = [m for m in messages if m["is_crush"]]
    user_msgs = [m for m in messages if not m["is_crush"]]

    if not crush_msgs:
        return {"error": f"未找到 '{crush_name}' 的消息，请检查名称是否正确"}

    # 消息长度统计
    crush_lengths = [len(m["content"]) for m in crush_msgs]
    avg_length = sum(crush_lengths) / len(crush_lengths) if crush_lengths else 0
    length_category = "short" if avg_length < 15 else ("medium" if avg_length < 50 else "long")

    # Emoji 统计
    all_emojis = []
    msgs_with_emoji = 0
    for m in crush_msgs:
        found = EMOJI_PATTERN.findall(m["content"])
        if found:
            msgs_with_emoji += 1
            all_emojis.extend(found)
    emoji_freq = msgs_with_emoji / len(crush_msgs) if crush_msgs else 0
    emoji_counter = Counter(all_emojis)

    # 笑的方式统计
    laugh_patterns = Counter()
    for m in crush_msgs:
        content = m["content"]
        if re.search(r"哈{2,}", content):
            laugh_patterns["哈哈哈"] += 1
        if re.search(r"[hH]{2,}", content):
            laugh_patterns["hhhh"] += 1
        if "笑死" in content:
            laugh_patterns["笑死"] += 1
        if "🤣" in content or "😂" in content:
            laugh_patterns["emoji笑"] += 1

    # 回复时间统计（仅在有时间戳时计算）
    response_times = []
    for i in range(1, len(messages)):
        curr = messages[i]
        prev = messages[i - 1]
        if (
            curr["is_crush"]
            and not prev["is_crush"]
            and curr.get("datetime")
            and prev.get("datetime")
        ):
            try:
                t_curr = datetime.fromisoformat(curr["datetime"])
                t_prev = datetime.fromisoformat(prev["datetime"])
                diff = (t_curr - t_prev).total_seconds() / 60  # 分钟
                if 0 < diff < 1440:  # 排除超过一天的间隔
                    response_times.append(diff)
            except (ValueError, TypeError):
                pass

    response_time_stats = {}
    if response_times:
        response_times.sort()
        response_time_stats = {
            "median_minutes": round(response_times[len(response_times) // 2], 1),
            "p25_minutes": round(response_times[len(response_times) // 4], 1),
            "p75_minutes": round(response_times[3 * len(response_times) // 4], 1),
            "sample_size": len(response_times),
        }

    # 话题发起统计（简单启发式：超过2小时间隔视为新话题）
    topic_initiations = {"crush": 0, "user": 0}
    for i, m in enumerate(messages):
        if i == 0:
            if m["is_crush"]:
                topic_initiations["crush"] += 1
            else:
                topic_initiations["user"] += 1
            continue
        prev = messages[i - 1]
        if m.get("datetime") and prev.get("datetime"):
            try:
                gap = (
                    datetime.fromisoformat(m["datetime"])
                    - datetime.fromisoformat(prev["datetime"])
                ).total_seconds() / 3600
                if gap > 2:
                    if m["is_crush"]:
                        topic_initiations["crush"] += 1
                    else:
                        topic_initiations["user"] += 1
            except (ValueError, TypeError):
                pass

    total_topics = topic_initiations["crush"] + topic_initiations["user"]
    initiation_ratio = (
        round(topic_initiations["crush"] / total_topics * 100)
        if total_topics > 0
        else None
    )

    # 标点习惯
    punctuation_counter = Counter()
    for m in crush_msgs:
        content = m["content"]
        for char in ["。", "！", "？", "…", "～", "~", ".", "!", "?"]:
            if char in content:
                punctuation_counter[char] += content.count(char)

    return {
        "total_messages": len(messages),
        "crush_messages": len(crush_msgs),
        "user_messages": len(user_msgs),
        "message_length": {
            "average_chars": round(avg_length, 1),
            "category": length_category,
        },
        "emoji": {
            "frequency": round(emoji_freq * 100, 1),
            "top_emojis": [e for e, _ in emoji_counter.most_common(5)],
        },
        "laugh_style": dict(laugh_patterns.most_common(3)),
        "response_time": response_time_stats,
        "initiation_ratio": {
            "crush_pct": initiation_ratio,
            "total_topics": total_topics,
        },
        "punctuation": dict(punctuation_counter.most_common(5)),
        "data_quality": {
            "has_timestamps": any(m.get("datetime") for m in messages),
            "crush_msg_count": len(crush_msgs),
            "confidence_level": (
                "observed" if len(crush_msgs) >= 30
                else "inferred" if len(crush_msgs) >= 10
                else "speculative"
            ),
        },
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--stdin":
        crush_name = sys.argv[2] if len(sys.argv) >= 3 else "crush"
        text = sys.stdin.read()
    else:
        file_path = Path(sys.argv[1])
        crush_name = sys.argv[2] if len(sys.argv) >= 3 else "crush"
        if not file_path.exists():
            print(f"错误: 文件不存在: {file_path}")
            sys.exit(1)
        text = file_path.read_text(encoding="utf-8")

    messages = parse_messages(text, crush_name)

    if not messages:
        print(json.dumps({"error": "未能解析出任何消息，请检查格式"}, ensure_ascii=False))
        sys.exit(1)

    stats = compute_statistics(messages, crush_name)

    result = {
        "messages": messages,
        "statistics": stats,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
