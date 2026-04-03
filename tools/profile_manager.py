#!/usr/bin/env python3
"""
Crush Profile Manager — 档案 CRUD + 版本管理

用法:
    python profile_manager.py create <nickname> <json_file>
    python profile_manager.py load <nickname>
    python profile_manager.py update <nickname> <json_file>
    python profile_manager.py patch <nickname> <json_file_or_->   # 局部更新（合并）
    python profile_manager.py delete <nickname>
    python profile_manager.py list
    python profile_manager.py history <nickname>
    python profile_manager.py rollback <nickname> <version>
"""

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

PROFILES_DIR = Path(".crush-profiles")


def get_profile_dir(nickname: str) -> Path:
    """获取指定 crush 的档案目录"""
    slug = nickname.lower().replace(" ", "-")
    return PROFILES_DIR / slug


def create(nickname: str, data_path: str) -> None:
    """创建新档案"""
    profile_dir = get_profile_dir(nickname)
    if profile_dir.exists():
        print(f"错误: '{nickname}' 的档案已存在。使用 update 命令更新。")
        sys.exit(1)

    profile_dir.mkdir(parents=True)
    versions_dir = profile_dir / "versions"
    versions_dir.mkdir()

    with open(data_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    profile["nickname"] = nickname
    profile["created_at"] = datetime.now().strftime("%Y-%m-%d")
    profile["updated_at"] = profile["created_at"]
    profile.setdefault("version", "1.0")

    # 保存当前版本
    current_path = profile_dir / "profile.json"
    with open(current_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    # 保存版本备份
    version_name = f"v1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy2(current_path, versions_dir / version_name)

    print(f"已创建 '{nickname}' 的档案: {current_path}")


def load(nickname: str) -> None:
    """读取档案并输出"""
    profile_dir = get_profile_dir(nickname)
    current_path = profile_dir / "profile.json"

    if not current_path.exists():
        print(f"错误: 未找到 '{nickname}' 的档案。")
        sys.exit(1)

    with open(current_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    print(json.dumps(profile, ensure_ascii=False, indent=2))


def update(nickname: str, data_path: str) -> None:
    """更新档案，自动保存旧版本"""
    profile_dir = get_profile_dir(nickname)
    current_path = profile_dir / "profile.json"
    versions_dir = profile_dir / "versions"

    if not current_path.exists():
        print(f"错误: 未找到 '{nickname}' 的档案。使用 create 命令创建。")
        sys.exit(1)

    # 备份当前版本
    with open(current_path, "r", encoding="utf-8") as f:
        old_profile = json.load(f)

    version_num = len(list(versions_dir.glob("v*.json"))) + 1
    version_name = f"v{version_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy2(current_path, versions_dir / version_name)

    # 写入新数据
    with open(data_path, "r", encoding="utf-8") as f:
        new_profile = json.load(f)

    new_profile["nickname"] = nickname
    new_profile["created_at"] = old_profile.get("created_at", datetime.now().strftime("%Y-%m-%d"))
    new_profile["updated_at"] = datetime.now().strftime("%Y-%m-%d")
    new_profile["version"] = f"{version_num}.0"

    with open(current_path, "w", encoding="utf-8") as f:
        json.dump(new_profile, f, ensure_ascii=False, indent=2)

    print(f"已更新 '{nickname}' 的档案 (v{version_num})")


def list_profiles() -> None:
    """列出所有档案"""
    if not PROFILES_DIR.exists():
        print("暂无档案。")
        return

    profiles = []
    for d in sorted(PROFILES_DIR.iterdir()):
        if d.is_dir():
            profile_path = d / "profile.json"
            if profile_path.exists():
                with open(profile_path, "r", encoding="utf-8") as f:
                    p = json.load(f)
                profiles.append({
                    "nickname": p.get("nickname", d.name),
                    "created": p.get("created_at", "?"),
                    "updated": p.get("updated_at", "?"),
                    "version": p.get("version", "?"),
                })

    if not profiles:
        print("暂无档案。")
        return

    print(f"{'代号':<15} {'创建日期':<12} {'更新日期':<12} {'版本':<8}")
    print("-" * 50)
    for p in profiles:
        print(f"{p['nickname']:<15} {p['created']:<12} {p['updated']:<12} {p['version']:<8}")


def history(nickname: str) -> None:
    """查看档案版本历史"""
    profile_dir = get_profile_dir(nickname)
    versions_dir = profile_dir / "versions"

    if not versions_dir.exists():
        print(f"错误: 未找到 '{nickname}' 的档案。")
        sys.exit(1)

    versions = sorted(versions_dir.glob("v*.json"))
    if not versions:
        print("暂无历史版本。")
        return

    print(f"'{nickname}' 的版本历史:")
    for v in versions:
        stat = v.stat()
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"  {v.name:<30} {mtime}")


def delete(nickname: str) -> None:
    """删除档案"""
    profile_dir = get_profile_dir(nickname)
    if not profile_dir.exists():
        print(f"错误: 未找到 '{nickname}' 的档案。")
        sys.exit(1)

    shutil.rmtree(profile_dir)
    print(f"已删除 '{nickname}' 的档案。")


def patch(nickname: str, patch_json: str) -> None:
    """局部更新档案（合并而非覆盖）

    patch_json 可以是文件路径或 '-' 表示从 stdin 读取。
    只更新 patch 中包含的字段，保留其余字段不变。
    """
    profile_dir = get_profile_dir(nickname)
    current_path = profile_dir / "profile.json"
    versions_dir = profile_dir / "versions"

    if not current_path.exists():
        print(f"错误: 未找到 '{nickname}' 的档案。使用 create 命令创建。")
        sys.exit(1)

    # 备份当前版本
    with open(current_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    version_num = len(list(versions_dir.glob("v*.json"))) + 1
    version_name = f"v{version_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    shutil.copy2(current_path, versions_dir / version_name)

    # 读取 patch 数据
    if patch_json == "-":
        patch_data = json.loads(sys.stdin.read())
    else:
        with open(patch_json, "r", encoding="utf-8") as f:
            patch_data = json.load(f)

    # 递归合并
    def deep_merge(base: dict, overlay: dict) -> dict:
        for key, value in overlay.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    deep_merge(profile, patch_data)
    profile["updated_at"] = datetime.now().strftime("%Y-%m-%d")

    with open(current_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

    print(f"已局部更新 '{nickname}' 的档案 (v{version_num})")


def rollback(nickname: str, version: str) -> None:
    """回滚到指定版本"""
    profile_dir = get_profile_dir(nickname)
    versions_dir = profile_dir / "versions"
    current_path = profile_dir / "profile.json"

    # 模糊匹配版本
    matches = [v for v in versions_dir.glob("v*.json") if version in v.name]
    if not matches:
        print(f"错误: 未找到匹配 '{version}' 的版本。")
        sys.exit(1)
    if len(matches) > 1:
        print(f"错误: '{version}' 匹配到多个版本: {[m.name for m in matches]}")
        sys.exit(1)

    target = matches[0]

    # 先备份当前版本
    version_num = len(list(versions_dir.glob("v*.json"))) + 1
    backup_name = f"v{version_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_pre_rollback.json"
    shutil.copy2(current_path, versions_dir / backup_name)

    # 回滚
    shutil.copy2(target, current_path)
    print(f"已回滚 '{nickname}' 到 {target.name}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    commands = {
        "create": lambda: create(sys.argv[2], sys.argv[3]) if len(sys.argv) >= 4 else print("用法: create <nickname> <json_file>"),
        "load": lambda: load(sys.argv[2]) if len(sys.argv) >= 3 else print("用法: load <nickname>"),
        "update": lambda: update(sys.argv[2], sys.argv[3]) if len(sys.argv) >= 4 else print("用法: update <nickname> <json_file>"),
        "patch": lambda: patch(sys.argv[2], sys.argv[3]) if len(sys.argv) >= 4 else print("用法: patch <nickname> <json_file_or_->"),
        "delete": lambda: delete(sys.argv[2]) if len(sys.argv) >= 3 else print("用法: delete <nickname>"),
        "list": lambda: list_profiles(),
        "history": lambda: history(sys.argv[2]) if len(sys.argv) >= 3 else print("用法: history <nickname>"),
        "rollback": lambda: rollback(sys.argv[2], sys.argv[3]) if len(sys.argv) >= 4 else print("用法: rollback <nickname> <version>"),
    }

    if cmd in commands:
        commands[cmd]()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
