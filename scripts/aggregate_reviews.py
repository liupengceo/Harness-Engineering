#!/usr/bin/env python3
"""
聚合多份 review persona YAML 报告,产出一份面向人类的 markdown 评论。

约定:
  - 输入目录 (通过 --reports-dir) 下每个 review-<persona>.yaml 是一份
    按 templates/review-personas/README.md § 3 schema 写好的 YAML。
  - --triggered / --skipped 是 JSON 数组,描述调度决议。

聚合策略 (与 orchestrator.md 一致):
  - verdict 顶层汇总规则:
    any block      -> block
    any request-changes -> request-changes
    else any approve-with-changes -> approve-with-changes
    else all approve -> approve
  - any escalate_to_human -> 顶层挂 escalate 横幅
  - 按 severity 排序列 findings, 同 severity 保持出现顺序

输出: Markdown 到 stdout。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-not-found]
except ImportError:
    print("aggregate_reviews requires pyyaml", file=sys.stderr)
    sys.exit(1)

VERDICT_RANK = {
    "block": 0,
    "request-changes": 1,
    "approve-with-changes": 2,
    "approve": 3,
}

SEVERITY_RANK = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 4,
}


def roll_up_verdict(verdicts: list[str]) -> str:
    if not verdicts:
        return "approve"
    return min(verdicts, key=lambda v: VERDICT_RANK.get(v, 99))


def load_report(path: Path) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] failed to parse {path}: {exc}", file=sys.stderr)
        return None
    if not isinstance(data, dict):
        return None
    return data


def iter_reports(reports_dir: Path) -> list[tuple[str, dict[str, Any]]]:
    reports = []
    # Artifact downloads land under <reports_dir>/<artifact-name>/<file>
    # where artifact-name is like 'review-security'
    for sub in sorted(reports_dir.glob("review-*")):
        if sub.is_dir():
            for f in sorted(sub.glob("*.yaml")):
                data = load_report(f)
                if data:
                    reports.append((data.get("persona", sub.name), data))
        elif sub.suffix == ".yaml":
            data = load_report(sub)
            if data:
                reports.append((data.get("persona", sub.stem), data))
    return reports


def render_markdown(
    reports: list[tuple[str, dict[str, Any]]],
    triggered: list[str],
    skipped: list[str],
) -> str:
    if not reports:
        return (
            "## Review personas\n\n"
            "_No persona reports produced. This usually means `REVIEW_RUNNER` "
            "is unset/mis-configured, or all triggered jobs failed to run._\n"
        )

    verdicts = [r.get("verdict", "approve") for _, r in reports]
    top_verdict = roll_up_verdict(verdicts)

    lines: list[str] = []
    lines.append("## Review personas")
    lines.append("")
    lines.append(f"**Overall verdict:** `{top_verdict}`")
    lines.append("")
    lines.append(f"**Triggered** ({len(triggered)}): " + ", ".join(f"`{p}`" for p in triggered))
    if skipped:
        lines.append("")
        lines.append(f"**Skipped** ({len(skipped)}): " + ", ".join(f"`{p}`" for p in skipped))
    lines.append("")

    # Findings table
    findings_rows: list[tuple[int, str, str, str, str, str]] = []
    for persona, report in reports:
        for f in report.get("findings") or []:
            sev = (f.get("severity") or "info").lower()
            rank = SEVERITY_RANK.get(sev, 99)
            findings_rows.append(
                (
                    rank,
                    sev,
                    persona,
                    f.get("file", "") or "",
                    str(f.get("line", "") or ""),
                    (f.get("summary") or "").replace("|", "\\|"),
                )
            )
    findings_rows.sort(key=lambda r: (r[0], r[2]))

    if findings_rows:
        lines.append("### Findings")
        lines.append("")
        lines.append("| severity | persona | file | line | summary |")
        lines.append("|---|---|---|---|---|")
        for _, sev, persona, file, line, summary in findings_rows:
            lines.append(f"| `{sev}` | `{persona}` | `{file}` | {line} | {summary} |")
        lines.append("")
    else:
        lines.append("_No findings._")
        lines.append("")

    # Escalate banner
    escalate = [
        (p, r)
        for p, r in reports
        if (r.get("escalate_to_human") or {}).get("required")
    ]
    if escalate:
        lines.append("### Human attention required")
        lines.append("")
        for p, r in escalate:
            reason = (r.get("escalate_to_human") or {}).get("reason", "(no reason)")
            lines.append(f"- `{p}`: {reason}")
        lines.append("")

    # Followups
    followups: list[tuple[str, str]] = []
    for p, r in reports:
        for f in r.get("followups") or []:
            followups.append((p, str(f)))
    if followups:
        lines.append("### Followups")
        lines.append("")
        for p, f in followups:
            lines.append(f"- (_{p}_) {f}")
        lines.append("")

    # Per-persona summary
    lines.append("### Per-persona summary")
    lines.append("")
    lines.append("| persona | verdict | summary |")
    lines.append("|---|---|---|")
    for p, r in reports:
        v = r.get("verdict", "approve")
        s = (r.get("summary") or "").replace("|", "\\|")
        lines.append(f"| `{p}` | `{v}` | {s} |")
    lines.append("")

    lines.append("---")
    lines.append(
        "_Generated by `.github/workflows/review.yml`. "
        "Schema: `templates/review-personas/README.md § 3`. "
        "Runner config: repo variable `REVIEW_RUNNER`._"
    )
    return "\n".join(lines) + "\n"


def parse_json_array(src: str) -> list[str]:
    if not src:
        return []
    try:
        value = json.loads(src)
    except json.JSONDecodeError:
        return [s.strip() for s in src.split(",") if s.strip()]
    if isinstance(value, list):
        return [str(x) for x in value]
    return []


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reports-dir", type=Path, required=True)
    ap.add_argument("--triggered", type=str, default="[]")
    ap.add_argument("--skipped", type=str, default="[]")
    args = ap.parse_args(argv[1:])

    reports = iter_reports(args.reports_dir)
    triggered = parse_json_array(args.triggered)
    skipped = parse_json_array(args.skipped)

    print(render_markdown(reports, triggered, skipped), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
