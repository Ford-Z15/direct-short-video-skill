from pathlib import Path
import json
import re

SKILL_ROOT = Path(__file__).resolve().parents[1]
ENTRY_RE = re.compile(r"^#{2,4}\s+([A-Z]+-\d{3})｜", re.MULTILINE)
REFERENCE_RE = re.compile(r"`((?:references|data|scripts)/[^`\n]+?\.(?:md|json|py))`")
FORBIDDEN_TERMS = [
    "\u859b", "\u5c0f\u6e05\u65b0", "\u8840\u7070", "\u6d88\u6d88",
    "\u5f90\u8001\u5e08", "\u8096\u8001\u5e08", "\u54a9\u54a9", "\u6556\u4e91",
    "\u9178\u5976", "\u90b5\u8001\u5e08", "\u6c5f\u6e56\u8bf4", "xue" + "hui",
]


def main() -> None:
    errors = []
    skill_path = SKILL_ROOT / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not frontmatter_match:
        errors.append("SKILL.md 缺少有效 YAML frontmatter")
    else:
        fields = {}
        for line in frontmatter_match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                fields[key.strip()] = value.strip()
        if set(fields) != {"name", "description"}:
            errors.append("frontmatter 只能包含 name 和 description")
        if fields.get("name") != SKILL_ROOT.name:
            errors.append("name 必须与 Skill 文件夹一致")
        if not re.fullmatch(r"[a-z0-9-]{1,63}", fields.get("name", "")):
            errors.append("name 只能包含小写字母、数字和连字符")
        if len(fields.get("description", "")) < 60:
            errors.append("description 缺少完整功能或触发说明")

    knowledge_files = sorted((SKILL_ROOT / "references/knowledge").glob("*.md"))
    entry_count = sum(len(ENTRY_RE.findall(path.read_text(encoding="utf-8"))) for path in knowledge_files)
    if len(knowledge_files) != 16:
        errors.append(f"知识文件数量异常：{len(knowledge_files)}")
    if entry_count != 121:
        errors.append(f"知识条目数量异常：{entry_count}")

    for path in SKILL_ROOT.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        relative = path.relative_to(SKILL_ROOT)
        if "- **来源**：" in content or re.search(r"P\d{4}", content):
            errors.append(f"公开版仍含内部溯源：{relative}")
        if "course/transcripts" in content:
            errors.append(f"公开版仍引用内部文稿：{relative}")
        for match in REFERENCE_RE.finditer(content):
            reference = match.group(1)
            if not (SKILL_ROOT / reference).exists():
                errors.append(f"资源引用不存在：{relative} → {reference}")

    repo_root = SKILL_ROOT.parents[1]
    for path in repo_root.rglob("*"):
        if not path.is_file() or "dist" in path.parts:
            continue
        if path.suffix not in {".md", ".txt", ".json", ".py", ".gitignore"}:
            continue
        content = path.read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_TERMS:
            if term.lower() in content:
                errors.append(f"公开仓库存在禁用痕迹：{path.relative_to(repo_root)}")

    lexicon = json.loads((SKILL_ROOT / "data/compliance_lexicon.json").read_text(encoding="utf-8"))
    if not lexicon.get("reviewed_on") or not lexicon.get("groups"):
        errors.append("违禁词库缺少复核日期或分组")

    if errors:
        for error in errors:
            print(f"ERROR\t{error}")
        raise SystemExit(f"Skill 验证失败：{len(errors)} 个问题")

    print(f"SKILL_VALIDATED\t{SKILL_ROOT.name}")
    print(f"KNOWLEDGE_FILES\t{len(knowledge_files)}")
    print(f"ENTRIES\t{entry_count}")
    print("PUBLIC_SOURCES\tinternal transcripts excluded")


if __name__ == "__main__":
    main()
