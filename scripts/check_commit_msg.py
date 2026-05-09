#!/usr/bin/env python3
"""
检查 commit message 的 subject 行,见 .kiro/steering/git-workflow.md § 2。

允许格式:
    <type>(<scope>): <subject>
    <type>: <subject>              # scope 可选

type 白名单:
    feat fix docs style refactor perf test chore build ci harness security revert

subject 行长度 <= 72。
subject 不以句号结尾(祈使式)。
禁止 subject 为 "fix bug" / "update" / "wip" (忽略大小写)。

作为 commit-msg 阶段 hook;pre-commit 会把 commit message 文件路径作为 argv[1] 传入。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

TYPES = {
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "chore",
    "build",
    "ci",
    "harness",
    "security",
    "revert",
}

FORBIDDEN_SUBJECTS = {"fix bug", "update", "wip", "misc", "changes"}

# type(scope): subject   或    type: subject
SUBJECT_RE = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]+)\))?!?:\s+(?P<subject>.+)$"
)


def check(subject: str) -> list[str]:
    errors = []
    if len(subject) > 72:
        errors.append(f"subject > 72 chars (is {len(subject)})")
    if subject.endswith("."):
        errors.append("subject must not end with '.'")
    m = SUBJECT_RE.match(subject)
    if not m:
        errors.append(
            "subject does not match '<type>(<scope>): <subject>' or '<type>: <subject>'"
        )
        return errors
    t = m.group("type")
    if t not in TYPES:
        errors.append(
            f"type '{t}' not in allowed types {sorted(TYPES)}"
        )
    body = m.group("subject").strip()
    if body.lower() in FORBIDDEN_SUBJECTS:
        errors.append(f"subject '{body}' is too vague; write what & why")
    return errors


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return 0
    msg_file = Path(argv[1])
    if not msg_file.is_file():
        return 0
    first_line = ""
    for line in msg_file.read_text(encoding="utf-8").splitlines():
        if line.strip() == "":
            continue
        if line.lstrip().startswith("#"):
            continue
        first_line = line.rstrip()
        break

    # 允许 merge commit / revert commit 等由 git 自动生成的 prefix
    if first_line.startswith(("Merge ", "Revert ", "fixup! ", "squash! ")):
        return 0

    errors = check(first_line)
    if not errors:
        return 0
    print(f"commit subject: {first_line!r}")
    for e in errors:
        print(f"  - {e}")
    print("see .kiro/steering/git-workflow.md § 2 for the rule")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
