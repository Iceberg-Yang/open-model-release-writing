#!/usr/bin/env python3
"""Heuristic audit for Chinese open-model release articles.

This script finds mechanical and editorial risk signals. It does not verify facts,
URLs, benchmark mappings, or deployment commands against primary sources.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Finding:
    severity: str
    line: int | None
    code: str
    message: str


RISK_WORDS = {
    "最强": "Define the eligible comparison set, benchmark, setting, and date.",
    "SOTA": "Cite a dated leaderboard or evaluation proving the SOTA scope.",
    "全面领先": "A broad superiority claim requires a representative same-setting suite.",
    "全面超越": "Do not generalize selected benchmark wins to overall capability.",
    "比肩": "Limit the claim to named benchmarks or capability categories.",
    "大幅领先": "State the exact score difference and evaluation setting.",
    "表现更佳": "Name the comparison or ablation that demonstrates the improvement.",
}

HYPE_PATTERNS = {
    "震惊": "Remove sensational wording.",
    "竟然": "Replace emotional emphasis with a sourced fact.",
    "居然": "Replace emotional emphasis with a sourced fact.",
    "小编": "Use objective third-person language.",
    "本文将": "Open with who released what, not article meta-commentary.",
    "众所周知": "Remove unsupported universal framing.",
    "不言而喻": "State the evidence instead of asserting obviousness.",
}

GENERIC_ALT = re.compile(r"!\[(?:image(?:\.png)?|图片|截图|figure|fig)?\]", re.I)
HEADING_RE = re.compile(r"^ {0,3}(#{1,6})\s+(.+?)\s*$")
NUMBERED_SECTION_RE = re.compile(r"^##\s+0?(\d{1,2})[\s　]+")
LINK_RE = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
SEVERITY_RANK = {"blocker": 0, "major": 1, "minor": 2}
NOTICE = (
    "Heuristic checks only: passed reflects the severity threshold, not fact verification. "
    "Optional ModelScope checking only skips missing-link findings; it does not confirm listing status."
)


def line_number(text: str, position: int) -> int:
    return text.count("\n", 0, position) + 1


def audit(path: Path, modelscope: str = "required") -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    scan_text = text.replace("\u00a0", " ")
    scan_lines = [line.replace("\u00a0", " ") for line in lines]
    findings: list[Finding] = []

    nbsp_count = text.count("\u00a0")
    if nbsp_count:
        findings.append(
            Finding("minor", None, "NBSP", f"Found {nbsp_count} non-breaking spaces from document export.")
        )

    opening: tuple[int, str, str] | None = None
    code_blocks: list[tuple[int, int, str]] = []
    prose_lines = scan_lines.copy()
    has_bash = False
    for index, line in enumerate(scan_lines, 1):
        match = FENCE_RE.match(line)
        if opening is not None:
            prose_lines[index - 1] = ""
            start, marker, language = opening
            if (
                match
                and match.group(1)[0] == marker[0]
                and len(match.group(1)) >= len(marker)
                and not match.group(2).strip()
            ):
                code_blocks.append((start, index, language))
                opening = None
        elif match:
            marker, info = match.groups()
            # Backtick-fence info strings cannot contain backticks.
            if marker[0] == "`" and "`" in info:
                continue
            language = info.strip()
            opening = (index, marker, language)
            has_bash = has_bash or language.startswith("bash")
            prose_lines[index - 1] = ""

    if opening is not None:
        findings.append(Finding("blocker", opening[0], "FENCE", "Unclosed Markdown code fence."))

    # Keep blank lines for fences and code so prose finding line numbers stay intact.
    prose_text = "\n".join(prose_lines)
    for start, end, language in code_blocks:
        content_lines = max(0, end - start - 1)
        if not language:
            findings.append(Finding("minor", start, "CODE_LANG", "Code fence has no language tag."))
        if content_lines > 30:
            findings.append(
                Finding("minor", start, "CODE_LENGTH", f"Code block has {content_lines} lines; consider splitting it.")
            )

    for word, guidance in RISK_WORDS.items():
        for match in re.finditer(re.escape(word), prose_text, re.I):
            findings.append(
                Finding("major", line_number(prose_text, match.start()), "CLAIM_SCOPE", f"`{word}`: {guidance}")
            )

    for word, guidance in HYPE_PATTERNS.items():
        for match in re.finditer(re.escape(word), prose_text):
            findings.append(
                Finding("minor", line_number(prose_text, match.start()), "STYLE", f"`{word}`: {guidance}")
            )

    for index, line in enumerate(prose_lines, 1):
        if GENERIC_ALT.search(line):
            findings.append(Finding("minor", index, "ALT_TEXT", "Image has generic or empty alt text."))
        if "支持 Transformer 架构" in line:
            findings.append(
                Finding(
                    "major",
                    index,
                    "TRANSFORMERS_TERM",
                    "If software support is intended, write `已接入 Hugging Face Transformers`.",
                )
            )
        if "仅具备解码功能" in line:
            findings.append(
                Finding("minor", index, "DECODER_TERM", "Prefer the architecture term `仅解码器模型/架构`.")
            )
        if re.search(r"参数\s*W", line) or re.search(r"参数W", line):
            findings.append(Finding("minor", index, "SPACING", "Add a space between Chinese text and `W`."))

    # Deployment recipes and hardware signals still inspect the complete article.
    for index, line in enumerate(scan_lines, 1):
        if re.search(r"从源码构建\s*[^\n]+", line) and "commit" not in text.lower() and "checkout" not in text.lower():
            findings.append(
                Finding("major", index, "UNPINNED_SOURCE", "Source build is not pinned to a version or commit.")
            )

    sections: list[tuple[int, int]] = []
    for index, line in enumerate(prose_lines, 1):
        match = NUMBERED_SECTION_RE.match(line)
        if match:
            sections.append((index, int(match.group(1))))
    for (line_a, number_a), (line_b, number_b) in zip(sections, sections[1:]):
        if number_b != number_a + 1:
            findings.append(
                Finding("minor", line_b, "SECTION_ORDER", f"Section number jumps from {number_a:02d} to {number_b:02d}.")
            )

    headings = [
        (index, re.sub(r"\s+#+\s*$", "", match.group(2)).strip())
        for index, line in enumerate(prose_lines, 1)
        if (match := HEADING_RE.match(line)) and match.group(1) == "#"
    ]
    headings = [(index, title) for index, title in headings if title and not re.fullmatch(r"#+", title)]
    if not headings:
        findings.append(Finding("major", 1, "TITLE", "No non-empty Markdown H1 title found."))
    elif len(headings[0][1]) > 60:
        findings.append(Finding("minor", headings[0][0], "TITLE_LENGTH", "Title is longer than 60 characters."))

    if modelscope == "required" and "modelscope.cn/models/" not in scan_text:
        findings.append(Finding("major", None, "MODELSCOPE", "No ModelScope model link found."))

    if (has_bash or "```bash" in scan_text) and not re.search(r"(?:部署|推理|Inference|vLLM|SGLang)", scan_text, re.I):
        findings.append(Finding("minor", None, "DEPLOY_CONTEXT", "Bash commands appear without a deployment/inference section."))

    if re.search(r"git clone", scan_text) and not re.search(r"git (?:checkout|switch)\s+", scan_text):
        findings.append(
            Finding("major", None, "GIT_PIN", "A `git clone` deployment recipe has no pinned tag or commit.")
        )

    if re.search(r"(?:NVFP4|FP4)", scan_text, re.I) and not re.search(
        r"Blackwell|B200|B300|GB200|GB300", scan_text, re.I
    ):
        findings.append(
            Finding("major", None, "FP4_HARDWARE", "FP4/NVFP4 is mentioned without an explicit validated GPU family.")
        )

    if re.search(r"(?:MTP|num_speculative_tokens)", scan_text, re.I) and not re.search(
        r"Multi[- ]Token|多\s*Token|推测解码|草稿", scan_text, re.I
    ):
        findings.append(Finding("major", None, "MTP", "MTP is used but not explained."))

    if "100 万 Token" in scan_text or re.search(r"\b1M\s*(?:Token|tokens)", scan_text, re.I):
        if not re.search(r"KV\s*Cache|缓存|显存|context.*limit|上下文.*限制", scan_text, re.I | re.S):
            findings.append(
                Finding("minor", None, "LONG_CONTEXT", "Million-token context is mentioned without serving/memory caveats.")
            )

    urls = [target for _, target in LINK_RE.findall(scan_text)]
    temporary_urls = [url for url in urls if re.search(r"/var/folders/|TemporaryItems|/tmp/", url)]
    if temporary_urls:
        findings.append(Finding("blocker", None, "TEMP_URL", f"Found {len(temporary_urls)} temporary local link(s)."))

    local_absolute = [url for url in urls if url.startswith("/")]
    if local_absolute:
        findings.append(
            Finding("major", None, "LOCAL_LINK", f"Found {len(local_absolute)} absolute local link(s); replace before online publishing.")
        )

    if re.search(r"开放权重|开源", prose_text) and not re.search(
        r"许可证|license|Apache|MIT|模型卡|model card", prose_text, re.I
    ):
        findings.append(
            Finding("minor", None, "OPENNESS", "Openness is claimed without visible license/model-card context.")
        )

    architecture_training = re.search(
        r"^##[^\S\n]+[^\n]*架构与训练[^\n]*$(.*?)(?=^##[^\S\n]+|\Z)", prose_text, re.M | re.S
    )
    if architecture_training and not re.search(
        r"预训练|后训练|训练阶段|优化器|\bSFT\b|\bRL\b|rollout", architecture_training.group(1), re.I
    ):
        findings.append(
            Finding(
                "major",
                line_number(prose_text, architecture_training.start()),
                "SECTION_CONTENT",
                "Section title says `架构与训练`, but the section contains no substantive training discussion.",
            )
        )

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Heuristically audit a Chinese open-model release Markdown article.",
        epilog=NOTICE,
    )
    parser.add_argument("article", type=Path, help="Path to a Markdown article")
    parser.add_argument(
        "--modelscope", choices=("required", "optional"), default="required",
        help="Missing ModelScope link policy (default: required); optional does not confirm listing status",
    )
    parser.add_argument(
        "--fail-on", choices=tuple(SEVERITY_RANK), default="blocker",
        help="Fail on this severity or higher (default: blocker); not a fact-verification result",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format (default: text)")
    args = parser.parse_args()

    error = None
    findings: list[Finding] = []
    try:
        findings = audit(args.article, modelscope=args.modelscope)
    except (OSError, UnicodeError) as exc:
        error = f"Cannot read article: {exc}"

    findings.sort(key=lambda item: (SEVERITY_RANK[item.severity], item.line or 0, item.code))
    counts = {severity: sum(item.severity == severity for item in findings) for severity in SEVERITY_RANK}
    passed = None if error else not any(
        counts[severity] for severity in SEVERITY_RANK
        if SEVERITY_RANK[severity] <= SEVERITY_RANK[args.fail_on]
    )

    if args.format == "json":
        print(json.dumps({
            "article": str(args.article),
            "modelscope": args.modelscope,
            "fail_on": args.fail_on,
            "findings": [asdict(item) for item in findings],
            "counts": counts,
            "passed": passed,
            "error": error,
            "notice": NOTICE,
        }, ensure_ascii=False, indent=2))
    elif error:
        print(f"ERROR: {error}", file=sys.stderr)
    else:
        print(
            f"Audit: {args.article}\n"
            f"Findings: {counts['blocker']} blocker, {counts['major']} major, {counts['minor']} minor\n"
            f"Passed: {passed} (fail-on: {args.fail_on}; modelscope: {args.modelscope})\n"
            f"{NOTICE}"
        )
        for item in findings:
            location = f"line {item.line}" if item.line else "document"
            print(f"[{item.severity.upper()}] {item.code} ({location}): {item.message}")

    return 2 if error else (0 if passed else 1)


if __name__ == "__main__":
    raise SystemExit(main())
