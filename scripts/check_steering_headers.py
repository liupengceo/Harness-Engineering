#!/usr/bin/env python3
"""
检查 .kiro/steering/*.md 的 front-matter。

要求(见 .kiro/steering/README.md § 格式约定):
  - 必有 YAML front-matter。
  - 必含 `title`。
  - 必含 `inclusion`,取值:always | manual | fileMatch。
  - 若 inclusion=fileMatch,必须同时有 fileMatchPattern。
  - DEPRECATION.md / README.md 允许豁免(白名单)。

这条 hook 是一条"机器可验证的 steering"(替代 harness-steward persona
里重复出现的人工检查项)。
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml  # type: ignore[import-not-found]
except ImportError:
    yaml = None  # type: ignore[assignment]

ALLOWED_INCLUSION = {"always", "manual", "fileMatch"}
EXEMPT = {".kiro/steering/README.md", ".kiro/steering/DEPRECATION.md"}


def split_front_matter(text: str) -> tuple[dict | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm_text = text[3:end].strip()
    body = text[end + 4 :]
    if yaml is None:
        raise RuntimeError("pyyaml is required to parse steering front-matter")
    try:
        data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as exc:
        raise SystemExit(f"invalid YAML front-matter: {exc}") from exc
    if not isinstance(data, dict):
        return None, text
    return data, body


def check(path: Path) -> list[str]:
    rel = path.as_posix()
    if rel in EXEMPT:
        return []

    text = path.read_text(encoding="utf-8")
    fm, _ = split_front_matter(text)
    errors: list[str] = []
    if fm is None:
        errors.append(f"{rel}: missing YAML front-matter (---)")
        return errors
    if "title" not in fm or not str(fm.get("title", "")).strip():
        errors.append(f"{rel}: front-matter missing non-empty `title`")
    inclusion = fm.get("inclusion")
    if inclusion not in ALLOWED_INCLUSION:
        errors.append(
            f"{rel}: `inclusion` must be one of {sorted(ALLOWED_INCLUSION)}, got {inclusion!r}"
        )
    if inclusion == "fileMatch" and not fm.get("fileMatchPattern"):
        errors.append(
            f"{rel}: inclusion=fileMatch requires `fileMatchPattern`"
        )
    return errors


def main(argv: list[str]) -> int:
    if len(argv) <= 1:
        return 0
    if yaml is None:
        print(
            "check_steering_headers: PyYAML missing; skipped. "
            "Install pyyaml>=6.0 to enable this hook.",
            file=sys.stderr,
        )
        return 0
    rc = 0
    for arg in argv[1:]:
        p = Path(arg)
        if not p.is_file():
            continue
        for err in check(p):
            print(err)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
