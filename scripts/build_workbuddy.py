#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 skills/sdskill 合并为 WorkBuddy 单文件版。

用法（仓库根目录）：
    python scripts/build_workbuddy.py

产物：workbuddy/sdskill-workbuddy.md
- 不修改 skills/sdskill 下任何源文件。
- 将「读取 references/...」类路径引用改写为本文章节引用。
- 附录内嵌违禁词库 JSON，供无脚本环境逐项检查。
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "sdskill"
OUT = ROOT / "workbuddy" / "sdskill-workbuddy.md"

PROMPT_ORDER = [
    "director_core",
    "intake_dialogue",
    "director_analysis",
    "compliance_review",
    "visual_delivery",
]

KNOWLEDGE_ORDER = [
    "positioning",
    "ip_positioning",
    "research",
    "topic_selection",
    "hooks",
    "script_templates",
    "copywriting",
    "storyboarding",
    "filming",
    "editing",
    "editing_advanced",
    "publishing",
    "sales_scripts",
    "platform_operations",
    "paid_promotion",
    "live_commerce",
]

HEADER = """# 抖音短视频编导专家（WorkBuddy 单文件版）

> 本文件由 `scripts/build_workbuddy.py` 从 `skills/sdskill/` 自动合并生成，内容以源文件为准。
> 适用：WorkBuddy 等不支持按路径读取文件、不可运行 Python 的对话型智能体。
> 用法：将本文件完整上传为知识库附件，自定义指令见仓库 README「在 WorkBuddy 中使用」。
> 与标准版的差异：① 「读取 references/...」已改为查阅本文对应章节；② 不运行任何脚本，违禁词按附录词库逐项人工核对；③ 版本自检不执行，更新以 GitHub Releases 页面为准。
> 章节名即原文件名（不含扩展名），例如「director_core」对应原 `references/prompts/director_core.md`。

---

"""


def rewrite_paths(text):
    """把 references 与 data 路径引用改为本文章节引用。"""
    text = re.sub(
        r"`?references/(prompts|knowledge)/([a-z_]+)\.md`?",
        lambda m: "本文「%s」章节" % m.group(2),
        text,
    )
    text = re.sub(
        r"`?data/compliance_lexicon\.json`?",
        "本文附录「违禁词库」",
        text,
    )
    return text


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def demote_headings(text, levels=1):
    """章节内标题统一下移，避免与单文件的一级章节冲突。"""
    prefix = "#" * levels
    return re.sub(r"^(#{1,5}) ", lambda m: prefix + m.group(1) + " ", text, flags=re.M)


def chapter(title, body):
    return "\n\n---\n\n# 章节：%s\n\n%s\n" % (title, demote_headings(body.strip()))


def main():
    parts = [HEADER]

    skill_md = strip_frontmatter((SKILL / "SKILL.md").read_text(encoding="utf-8"))
    parts.append(rewrite_paths(skill_md).strip() + "\n")

    for name in PROMPT_ORDER:
        p = SKILL / "references" / "prompts" / (name + ".md")
        parts.append(chapter(name, rewrite_paths(p.read_text(encoding="utf-8"))))

    for name in KNOWLEDGE_ORDER:
        p = SKILL / "references" / "knowledge" / (name + ".md")
        parts.append(chapter(name, rewrite_paths(p.read_text(encoding="utf-8"))))

    lexicon = (SKILL / "data" / "compliance_lexicon.json").read_text(encoding="utf-8")
    json.loads(lexicon)  # 校验 JSON 有效
    parts.append(
        "\n\n---\n\n# 附录：违禁词库\n\n"
        "无脚本环境下，对待交付文案先做 Unicode NFKC 规范化，再按以下词条逐项字面检查；命中后结合语境与证据复核，未命中不等于合规。\n\n"
        "```json\n" + lexicon.strip() + "\n```\n"
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    content = "".join(parts)
    OUT.write_text(content, encoding="utf-8")
    print("WROTE", OUT)
    print("chars:", len(content))
    leftover = re.findall(r"references/(?:prompts|knowledge)/[a-z_]+\.md", content)
    print("unrewritten refs:", leftover)


if __name__ == "__main__":
    main()
