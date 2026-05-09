#!/usr/bin/env python3
"""
Persona 调度器。

输入:
  - stdin 或 --diff-files 参数:一行一个路径,当前 PR 改动的文件列表
  - --labels 参数(可选):PR 的 labels,逗号分隔

输出:
  - stdout:JSON,形如
      {
        "triggered": ["security", "testing", "harness-steward"],
        "skipped":   ["performance", "observability", "api-design", "docs"],
        "reasons":   {"security": "...", "testing": "...", ...}
      }

规则来自 /templates/review-personas/README.md § 7 与 orchestrator.md。
保持与那份文档严格一致;如需更动,先改文档再改脚本(harness-change PR)。

使用:
  git diff --name-only origin/main...HEAD | python3 scripts/select_personas.py
  python3 scripts/select_personas.py --diff-files changes.txt --labels harness-change,security
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# 永远必跑的 persona
ALWAYS_ON = ["security", "testing"]

# 基于 path 的触发规则;每条规则 = (persona, 匹配该 persona 的 path 正则, 触发理由)
PATH_RULES: list[tuple[str, re.Pattern[str], str]] = [
    (
        "api-design",
        re.compile(r"(^|/)(routes|handlers|controllers|schemas?|api|openapi|grpc|proto)/", re.I),
        "touches public interface / schema layer",
    ),
    (
        "api-design",
        re.compile(r"\.(proto|openapi\.ya?ml|openapi\.json|graphql)$", re.I),
        "touches API schema file",
    ),
    (
        "performance",
        re.compile(r"(^|/)(bench|perf|critical|hot|workers?)/", re.I),
        "touches performance-critical directory",
    ),
    (
        "observability",
        re.compile(r"(^|/)(logging|metrics|tracing|observability|alerts?)/", re.I),
        "touches observability directory",
    ),
    (
        "observability",
        re.compile(r"(dashboard|alert)s?\.(ya?ml|json|tf)$", re.I),
        "touches dashboard / alert definition",
    ),
    (
        "docs",
        re.compile(r"(^|/)(docs?|adr|runbooks?)/", re.I),
        "touches documentation",
    ),
    (
        "docs",
        re.compile(r"(?:^|/)CHANGELOG\.md$", re.I),
        "touches CHANGELOG",
    ),
    (
        "harness-steward",
        re.compile(r"^(AGENTS\.md|\.kiro/|templates/|\.github/(workflows|pull_request_template\.md|ISSUE_TEMPLATE)|scripts/check_.*\.py)"),
        "touches harness surface (AGENTS / steering / templates / CI / guards)",
    ),
]

ALL_PERSONAS = [
    "security",
    "testing",
    "api-design",
    "performance",
    "observability",
    "docs",
    "harness-steward",
]


def parse_diff_files(source: str) -> list[str]:
    files = [line.strip() for line in source.splitlines() if line.strip()]
    # 去掉 "A\t" / "M\t" 前缀(`git diff --name-status` 模式)
    cleaned: list[str] = []
    for f in files:
        parts = f.split("\t")
        cleaned.append(parts[-1])
    return cleaned


def pick(files: list[str], labels: set[str]) -> dict:
    triggered: dict[str, str] = {p: "" for p in ALWAYS_ON}
    for p in ALWAYS_ON:
        triggered[p] = "always-on per templates/review-personas/README.md § 7"

    # Label-based overrides
    if "harness-change" in labels:
        triggered["harness-steward"] = "PR label: harness-change"
    if "security" in labels:
        triggered["security"] = "PR label: security (already always-on; elevated)"
    if "performance" in labels:
        triggered["performance"] = "PR label: performance"

    # Path-based triggers
    for path in files:
        for persona, pattern, reason in PATH_RULES:
            if persona in triggered:
                continue
            if pattern.search(path):
                triggered[persona] = f"path matches {pattern.pattern!r} (e.g. {path})"

    skipped = [p for p in ALL_PERSONAS if p not in triggered]
    return {
        "triggered": [p for p in ALL_PERSONAS if p in triggered],
        "skipped": skipped,
        "reasons": {p: triggered[p] for p in ALL_PERSONAS if p in triggered},
    }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--diff-files",
        type=Path,
        default=None,
        help="file containing 'git diff --name-only' output; default: stdin",
    )
    ap.add_argument(
        "--labels",
        type=str,
        default="",
        help="comma-separated PR labels",
    )
    ap.add_argument(
        "--pretty",
        action="store_true",
        help="pretty-print the JSON output",
    )
    args = ap.parse_args(argv[1:])

    if args.diff_files:
        text = args.diff_files.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    files = parse_diff_files(text)
    labels = {s.strip() for s in args.labels.split(",") if s.strip()}

    result = pick(files, labels)
    kwargs: dict = {"ensure_ascii": False}
    if args.pretty:
        kwargs["indent"] = 2
    print(json.dumps(result, **kwargs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
