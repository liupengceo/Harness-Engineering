#!/usr/bin/env python3
"""
Check whether a PR has an ExecPlan (or qualifies for exemption).

The rule, codified from AGENTS.md § 3.1:
  "Any task that touches production code must produce an ExecPlan first,
   placed as the first commit of the PR or in the PR description."

This script is intentionally *conservative*: it flags PRs that appear to
lack a plan, but does NOT block merges. Branch protection can promote the
resulting status check to required-for-merge at the repo's discretion.

Usage
-----
  check_pr_has_execplan.py
    --changed-files <path>      # one relative path per line
    --pr-body <path>            # the PR description body (markdown)
    --pr-title <str>            # PR title (for conventional-commit typing)
    --pr-labels <str>           # comma-separated labels (e.g. "fix,docs")

Exits
-----
  0  PR has a plan OR qualifies for an exemption
  1  PR touches production code without a plan
  2  Arguments are wrong / input files unreadable

The exit code is what CI reads. Also emits a human-readable summary on
stdout, which the workflow pastes into a sticky PR comment.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# -----------------------------------------------------------------------
# Policy constants. Tune here, not in the workflow.
# -----------------------------------------------------------------------

# Files whose changes TRIGGER the ExecPlan requirement.
CODE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".kt",
    ".swift", ".rb", ".c", ".h", ".cpp", ".hpp", ".cs", ".scala",
    ".php", ".erl", ".ex", ".clj", ".lua",
}

# Paths that are NEVER code for this purpose (even if they contain .py/.ts).
# These have their own harness-change gate (FU-4 PR template).
NON_CODE_PREFIXES = (
    "plan/",
    "docs/",
    ".github/",
    ".kiro/",
    "templates/",
    "tests/",            # tests-only PR should still have a plan? see below
    "test/",
    "scripts/",          # scripts are harness tooling, not product code
    ".",                 # dotfiles at repo root (.gitignore, .pre-commit-*)
)

# Types / labels that exempt a PR entirely.
EXEMPT_COMMIT_TYPES = {"docs", "chore", "ci", "build", "style", "revert"}

# PR-body markers that count as "the plan is here".
# (ExecPlan or 执行计划 section heading, or a reference to plan/execplans/).
BODY_MARKERS: list[re.Pattern[str]] = [
    re.compile(r"<!--\s*ExecPlan\s*-->", re.IGNORECASE),
    re.compile(r"^##+\s*ExecPlan\b", re.MULTILINE | re.IGNORECASE),
    re.compile(r"^##+\s*执行计划\b", re.MULTILINE),
    re.compile(r"`?plan/execplans/[\w\-/.]+\.md`?"),
]

# Very small PRs are always exempt (typo threshold).
TYPO_LOC_THRESHOLD = 10


# -----------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------

def is_code_file(path: str) -> bool:
    # Normalize Windows separators just in case.
    p = path.replace("\\", "/")
    # Starts-with any non-code prefix -> not code for this purpose.
    for prefix in NON_CODE_PREFIXES:
        if p == prefix.rstrip("/") or p.startswith(prefix):
            return False
    # Check extension.
    suffix = Path(p).suffix.lower()
    return suffix in CODE_EXTENSIONS


def parse_subject_type(title: str) -> str | None:
    """
    Extract `type` from a Conventional-Commit-ish title.
    e.g. "fix(auth): refresh token" -> "fix"
    Returns None if the title doesn't match.
    """
    m = re.match(r"^([a-z]+)(?:\([^)]+\))?!?:\s+\S", title)
    return m.group(1) if m else None


def check_body_for_plan(body: str) -> bool:
    for pat in BODY_MARKERS:
        if pat.search(body):
            return True
    return False


def check_diff_for_plan_file(changed_files: list[str]) -> str | None:
    """
    Return the first `plan/execplans/*.md` path present in the diff, or None.
    """
    for f in changed_files:
        f_norm = f.replace("\\", "/")
        if (
            f_norm.startswith("plan/execplans/")
            and f_norm.endswith(".md")
            and not f_norm.endswith(".gitkeep")
        ):
            return f_norm
    return None


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def evaluate(
    changed_files: list[str],
    pr_body: str,
    pr_title: str,
    pr_labels: list[str],
    approximate_loc: int | None = None,
) -> tuple[int, str]:
    """
    Returns (exit_code, markdown_summary).
    """
    lines: list[str] = []
    lines.append("## ExecPlan gate")
    lines.append("")

    # 1. Code touch?
    code_files = [f for f in changed_files if is_code_file(f)]
    if not code_files:
        lines.append(":white_check_mark: **Pass.** No production code files "
                     "changed. PR only touches docs / plan / .kiro / .github "
                     "/ templates / scripts / tests — these follow other "
                     "gates (see `AGENTS.md § 3.4`).")
        lines.append("")
        return 0, "\n".join(lines)

    # 2. Type-based exemption?
    title_type = parse_subject_type(pr_title)
    if title_type in EXEMPT_COMMIT_TYPES:
        lines.append(f":white_check_mark: **Pass.** PR subject type "
                     f"`{title_type}` is exempt from ExecPlan requirement "
                     f"(see `AGENTS.md § 3.1` and `.kiro/steering/"
                     f"git-workflow.md § 2`).")
        lines.append("")
        return 0, "\n".join(lines)

    # 3. Label-based exemption?
    exempt_labels = set(pr_labels) & (EXEMPT_COMMIT_TYPES | {"typo", "trivial"})
    if exempt_labels:
        lines.append(f":white_check_mark: **Pass.** PR labels "
                     f"{sorted(exempt_labels)} exempt this from the rule.")
        lines.append("")
        return 0, "\n".join(lines)

    # 4. LOC-based exemption?
    if approximate_loc is not None and approximate_loc <= TYPO_LOC_THRESHOLD:
        lines.append(f":white_check_mark: **Pass.** PR touches only "
                     f"{approximate_loc} lines (typo threshold "
                     f"{TYPO_LOC_THRESHOLD}).")
        lines.append("")
        return 0, "\n".join(lines)

    # 5. Is there a plan?
    plan_file = check_diff_for_plan_file(changed_files)
    if plan_file:
        lines.append(f":white_check_mark: **Pass.** ExecPlan found in the "
                     f"diff: `{plan_file}`.")
        lines.append("")
        return 0, "\n".join(lines)

    if check_body_for_plan(pr_body):
        lines.append(":white_check_mark: **Pass.** PR description references "
                     "an ExecPlan (via `<!-- ExecPlan -->` / `## ExecPlan` / "
                     "`## 执行计划` / a `plan/execplans/...` path).")
        lines.append("")
        return 0, "\n".join(lines)

    # 6. No plan and no exemption. Flag.
    lines.append(":x: **Fail.** This PR touches production code but has "
                 "neither an ExecPlan file in `plan/execplans/` nor an "
                 "ExecPlan block in the description. See `AGENTS.md § 3.1`.")
    lines.append("")
    lines.append("**Files that triggered the check:**")
    lines.append("")
    for f in code_files[:20]:
        lines.append(f"- `{f}`")
    if len(code_files) > 20:
        lines.append(f"- ... and {len(code_files) - 20} more")
    lines.append("")
    lines.append("**How to resolve:**")
    lines.append("")
    lines.append("1. Copy `templates/ExecPlan.md` to "
                 "`plan/execplans/<YYYYMMDD>-<slug>.md` and fill it.")
    lines.append("2. Commit it (ideally as the **first** commit of this PR; "
                 "if not, as a new commit is fine too).")
    lines.append("3. OR: paste a plan block into the PR description with one "
                 "of the markers `<!-- ExecPlan -->`, `## ExecPlan`, "
                 "`## 执行计划`, or a `plan/execplans/<file>.md` reference.")
    lines.append("4. OR: if this is genuinely exempt, add a "
                 "`docs` / `chore` / `ci` / `typo` label and this gate "
                 "will pass on the next sync.")
    lines.append("")
    return 1, "\n".join(lines)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--changed-files", type=Path, required=True)
    ap.add_argument("--pr-body", type=Path, required=True)
    ap.add_argument("--pr-title", type=str, required=True)
    ap.add_argument("--pr-labels", type=str, default="")
    ap.add_argument("--approx-loc", type=int, default=None)
    ap.add_argument("--out", type=Path, default=None,
                    help="write the markdown summary here (default: stdout)")
    args = ap.parse_args(argv[1:])

    try:
        changed_files = [
            ln.strip() for ln in args.changed_files.read_text().splitlines()
            if ln.strip()
        ]
        body = args.pr_body.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error reading inputs: {exc}", file=sys.stderr)
        return 2

    labels = [s.strip() for s in args.pr_labels.split(",") if s.strip()]

    code, summary = evaluate(
        changed_files, body, args.pr_title, labels, args.approx_loc
    )

    if args.out:
        args.out.write_text(summary + "\n", encoding="utf-8")
    else:
        print(summary)

    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
