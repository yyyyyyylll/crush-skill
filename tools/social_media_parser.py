#!/usr/bin/env python3
"""
社交媒体信息解析器

从社交媒体内容（文本粘贴或截图）中提取 crush 的性格线索和互动信号。

支持平台: 微信朋友圈、微博、小红书、抖音、Instagram

用法:
    python social_media_parser.py <file_path>
    python social_media_parser.py --stdin  # 从标准输入读取粘贴的文本
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path


ANALYSIS_GUIDE = """
## 社交媒体分析指引

### 可分析的信息类型

1. **Crush 的发布内容**
   - 发布频率 → 推断社交活跃度
   - 内容主题 → 推断兴趣爱好（Layer 3 enthusiasm_topics）
   - 配文风格 → 推断表达习惯（Layer 2 参考）
   - 自拍/生活照比例 → 推断自信度和分享欲

2. **Crush 与用户的互动**
   - 点赞频率 → 关注程度
   - 评论内容 → 互动质量
   - 是否秒赞 → 特别关注信号
   - Stories/动态查看速度 → 关注程度
   - 是否评论后又删除 → 纠结/在意的信号

3. **Crush 的社交风格基线**
   - TA 对其他人也这么热情吗？（区分社交风格 vs 特殊对待）
   - TA 的朋友圈权限设置（全部可见/三天可见/分组可见）
   - TA 的互动活跃度（到处点赞评论 vs 很少互动）
"""


def parse_social_text(text: str) -> dict:
    """从粘贴的社交媒体文本中提取基本信息"""

    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]

    # 尝试提取时间信息
    timestamps = []
    time_pattern = re.compile(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}")
    for line in lines:
        matches = time_pattern.findall(line)
        timestamps.extend(matches)

    # 提取话题标签
    hashtags = re.findall(r"#([^#\s]+)#?", text)

    # 提取 @提及
    mentions = re.findall(r"@(\S+)", text)

    # emoji 统计
    emoji_pattern = re.compile(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF"
        r"\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF"
        r"\U00002600-\U000026FF]+",
        flags=re.UNICODE,
    )
    emojis = emoji_pattern.findall(text)
    emoji_counter = Counter(emojis)

    # 基本内容分析
    total_chars = len(text)
    total_lines = len(lines)

    return {
        "raw_text_length": total_chars,
        "line_count": total_lines,
        "timestamps_found": timestamps,
        "hashtags": hashtags,
        "mentions": mentions,
        "emojis": {
            "total": len(emojis),
            "unique": list(emoji_counter.keys())[:10],
        },
        "content_preview": text[:500] + ("..." if len(text) > 500 else ""),
        "analysis_guide": ANALYSIS_GUIDE,
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--stdin":
        text = sys.stdin.read()
    else:
        file_path = Path(sys.argv[1])
        if not file_path.exists():
            print(f"错误: 文件不存在: {file_path}")
            sys.exit(1)
        text = file_path.read_text(encoding="utf-8")

    if not text.strip():
        print(json.dumps({"error": "输入内容为空"}, ensure_ascii=False))
        sys.exit(1)

    result = parse_social_text(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
