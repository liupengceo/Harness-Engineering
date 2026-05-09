#!/usr/bin/env python3
"""
当本次 staged 改动涉及 .kiro/steering/*.md (除 DEPRECATION.md / README.md 外) 时,
如果没有同时 stage .kiro/steering/DEPRECATION.md,
就 **warn**(不 fail)提醒作者:新增/收紧 steering 条目通常需要 DEPRECATION 登记。

逻辑:
  - 如果没 stage 任何 steering  → 直接通过。
  - 如果 stage 了 DEPRECATION.md → 直接通过。
  - 否则打印 advisory,但 exit 0(作者可能只是措辞调整)。

这条 hook 故意是**非致命** 的:
  - fail 掉会让"打字错误修复"也被阻断;
  - 但 warn 能把"你是否想登记退役条件"推到作者眼前,把忘记登记的概率降到最低。

如果将来发现社区还是频繁忘写,升级为 fail,并在 DEPRECATION.md 登记一次。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def staged_files() -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def main() -> int:
    files = staged_files()
    steering_changed = [
        f
        for f in files
        if f.startswith(".kiro/steering/")
        and f.endswith(".md")
        and Path(f).name not in {"DEPRECATION.md", "README.md"}
    ]
    if not steering_changed:
        return 0
    if ".kiro/steering/DEPRECATION.md" in files:
        return 0

    banner = "-" * 60
    print(banner)
    print("[advisory] steering edits without DEPRECATION.md update")
    print(banner)
    for f in steering_changed:
        print(f"  - {f}")
    print()
    print("If this edit adds/tightens a constraint to oppose a current-model")
    print("failure mode, please add an entry to .kiro/steering/DEPRECATION.md")
    print("with a retirement condition.")
    print()
    print("If this is purely wording / typo / reordering, you can ignore this.")
    print("See .kiro/steering/DEPRECATION.md for the format.")
    print(banner)
    return 0   # advisory only


if __name__ == "__main__":
    sys.exit(main())
