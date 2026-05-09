#!/usr/bin/env python3
"""
检查 TODO / FIXME / HACK 的格式(见 .kiro/steering/code-style.md § 8)。

硬规定:
  TODO(@owner, issue-or-link, deadline-or-condition): <内容>
  FIXME(@owner, issue): <内容>
  HACK(@owner, removal-condition): <内容>

也即:标签后面 **必须** 紧跟一个 `(` 开头的括号段,里面至少包含:
  - 一个 @username (不要求真是 GitHub 用户,但必须是 @开头的 token)
  - 至少一个逗号分隔的附加项(issue / 日期 / 条件)

模板 / docs / 这个脚本本身是白名单。
这是一条 "fix the harness, not the output" 型 hook:
发现一次裸 TODO → 改代码,不是改 steering。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ( ) 段内至少有 "@foo" 且有一个逗号 -> 即至少 2 个项
PATTERN = re.compile(
    r"""
    (?P<tag>\bTODO|FIXME|HACK)           # 标签
    \(                                    # 必须立刻跟 (
    (?P<body>[^()\n]*)                    # 括号内内容
    \)
    """,
    re.VERBOSE,
)

# 用来识别 "裸 TODO" (标签后面没有括号)
BARE_PATTERN = re.compile(r"\b(TODO|FIXME|HACK)(?![A-Za-z0-9_(])")

WHITELIST_SUFFIXES = {
    ".md",
    ".markdown",
}

WHITELIST_PATHS = {
    "scripts/check_todo_format.py",
    "AGENTS.md",
    ".kiro/steering/code-style.md",
}


def is_whitelisted(path: Path) -> bool:
    rel = path.as_posix()
    if rel in WHITELIST_PATHS:
        return True
    return path.suffix.lower() in WHITELIST_SUFFIXES


def check_line(line: str) -> str | None:
    # 先找带括号的 TODO,拆出 body 检查
    errors = []
    for m in PATTERN.finditer(line):
        body = m.group("body")
        # 至少含一个 @xxx
        if not re.search(r"@\w[\w.\-]*", body):
            errors.append(
                f"{m.group('tag')} is missing @owner inside parentheses"
            )
            continue
        # 至少再有一个逗号(说明还有 issue / 日期 / 条件)
        if "," not in body:
            errors.append(
                f"{m.group('tag')} must include @owner AND "
                f"issue/deadline/condition separated by commas"
            )

    # 找裸 TODO(后面没跟括号)
    # 但只在没匹配到带括号版本时才报(避免重复)
    if not errors:
        # 剥掉匹配过的带括号 TODO,剩下的再找 bare
        stripped = PATTERN.sub("", line)
        if BARE_PATTERN.search(stripped):
            errors.append(
                "bare TODO/FIXME/HACK without (@owner, ...) is forbidden; "
                "see .kiro/steering/code-style.md § 8"
            )

    return "; ".join(errors) if errors else None


def check_file(path: Path) -> list[str]:
    if is_whitelisted(path):
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []  # 二进制 / 读不了,跳过
    errs: list[str] = []
    for idx, line in enumerate(text.splitlines(), 1):
        msg = check_line(line)
        if msg:
            errs.append(f"{path.as_posix()}:{idx}: {msg}")
    return errs


def main(argv: list[str]) -> int:
    rc = 0
    for arg in argv[1:]:
        p = Path(arg)
        if not p.is_file():
            continue
        for err in check_file(p):
            print(err)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
