import argparse
import json
from pathlib import Path
import unicodedata

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEXICON_PATH = PROJECT_ROOT / "data" / "compliance_lexicon.json"


def normalize(value: str) -> str:
    return unicodedata.normalize("NFKC", value).lower()


def main() -> None:
    parser = argparse.ArgumentParser(description="扫描短视频文案中的违禁与高风险词语")
    parser.add_argument("file", type=Path, help="待检查的 UTF-8 文本或 Markdown 文件")
    args = parser.parse_args()

    lexicon = json.loads(LEXICON_PATH.read_text(encoding="utf-8"))
    source_path = args.file if args.file.is_absolute() else Path.cwd() / args.file
    text = normalize(source_path.read_text(encoding="utf-8"))

    hits = []
    for group in lexicon["groups"]:
        group_hits = []
        for term in group["terms"]:
            normalized_term = normalize(term)
            start = 0
            while True:
                index = text.find(normalized_term, start)
                if index < 0:
                    break
                group_hits.append({
                    "term": term,
                    "index": index,
                    "end": index + len(normalized_term),
                    "group": group["category"],
                    "severity": group["severity"],
                    "action": group["action"],
                })
                start = index + len(normalized_term)

        # 同一类别的重叠命中只保留最长词语，避免重复报告。
        previous_end = -1
        for hit in sorted(group_hits, key=lambda item: (item["index"], -len(item["term"]))):
            if hit["index"] < previous_end:
                continue
            hits.append(hit)
            previous_end = hit["end"]

    hits.sort(key=lambda hit: (hit["index"], hit["group"]))
    print(f"FILE\t{source_path}")
    print(f"LEXICON_REVIEWED_ON\t{lexicon['reviewed_on']}")
    print(f"HITS\t{len(hits)}")
    for hit in hits:
        print(f"{hit['severity']}\t{hit['term']}\t{hit['group']}\t{hit['action']}")
    print("NOTICE\t仅完成字面初筛；未命中不等于合规，命中后仍需结合语境、证据及最新平台规则复核")


if __name__ == "__main__":
    main()
