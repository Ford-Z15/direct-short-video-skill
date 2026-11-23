#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sdskill 版本自检：对比本地版本与 GitHub 最新 Release。

用法（在 Skill 根目录下）：
    python scripts/check_update.py

输出协议（首行机器可读，供 Skill 启动规则判断）：
    UPDATE_CHECK_SKIP <days_left>        距上次检查不足检查周期
    UP_TO_DATE v<x.y.z>                  本地已是最新
    UPDATE_AVAILABLE remote=<r> local=<l>  有新版本（后续行为人类可读更新指引）
    UPDATE_CHECK_FAILED <reason>         网络或环境问题，静默跳过

退出码恒为 0：检查失败绝不阻断用户任务。
"""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = SKILL_ROOT / "data" / "version.json"
STATE_DIR = Path.home() / ".sdskill"
STATE_FILE = STATE_DIR / "last_update_check"

GITHUB_API = "https://api.github.com/repos/{repo}/releases/latest"
RELEASE_DL = "https://github.com/{repo}/releases/latest/download/{asset}"


def log(msg):
    print(msg)


def parse_version(text):
    text = (text or "").strip().lstrip("vV")
    parts = []
    for piece in text.split("."):
        digits = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def read_local_version():
    try:
        data = json.loads(VERSION_FILE.read_text(encoding="utf-8"))
        return data.get("version", "0.0.0"), data
    except Exception:
        return "0.0.0", {}


def read_last_check():
    try:
        return float(STATE_FILE.read_text(encoding="utf-8").strip())
    except Exception:
        return 0.0


def write_last_check():
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        STATE_FILE.write_text(str(time.time()), encoding="utf-8")
    except Exception:
        pass  # 状态不可写时只影响节流，不影响检查


def fetch_latest(repo):
    url = GITHUB_API.format(repo=repo)
    req = urllib.request.Request(url, headers={"User-Agent": "sdskill-update-check"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload.get("tag_name", ""), payload.get("body", "")


def main():
    local, cfg = read_local_version()
    interval = int(cfg.get("check_interval_days", 14) or 14)
    repo = cfg.get("repo", "Ford-Z15/sdskill")
    asset = cfg.get("release_asset", "sdskill.skill")

    elapsed_days = (time.time() - read_last_check()) / 86400.0
    if elapsed_days < interval:
        left = max(1, int(round(interval - elapsed_days)))
        log("UPDATE_CHECK_SKIP %d" % left)
        return 0

    try:
        remote_tag, remote_body = fetch_latest(repo)
    except Exception as exc:
        log("UPDATE_CHECK_FAILED %s" % type(exc).__name__)
        return 0

    write_last_check()

    remote = (remote_tag or "").strip()
    if not remote:
        log("UPDATE_CHECK_FAILED empty_release")
        return 0

    if parse_version(remote) <= parse_version(local):
        log("UP_TO_DATE v%s" % local)
        return 0

    url = RELEASE_DL.format(repo=repo, asset=asset)
    log("UPDATE_AVAILABLE remote=%s local=v%s" % (remote, local))
    log("")
    log("发现新版本 %s（当前 v%s）。" % (remote, local))
    if remote_body:
        first_lines = [l for l in remote_body.splitlines() if l.strip()][:6]
        log("更新内容：")
        for line in first_lines:
            log("  " + line)
        log("")
    log("更新方法：下载 %s 解压后覆盖你 AI 工具 Skills 目录中的 sdskill 文件夹。" % asset)
    log("Windows PowerShell：")
    log('  iwr -Uri "%s" -OutFile "$env:TEMP\\sdskill.zip"' % url)
    log('  Expand-Archive "$env:TEMP\\sdskill.zip" -DestinationPath "<你的Skills目录>\\sdskill" -Force')
    log("macOS / Linux：")
    log('  curl -L -o /tmp/sdskill.zip "%s"' % url)
    log('  unzip -o /tmp/sdskill.zip -d ~/.claude/skills/sdskill')
    log("")
    log("也可在本仓库 Releases 页面手动下载： https://github.com/%s/releases/latest" % repo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
