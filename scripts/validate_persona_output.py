#!/usr/bin/env python3
"""
Validate a single persona adapter's YAML output.

Used by `scripts/run_review_persona.sh` as a guard at the end of every
runner branch: if the adapter returns malformed output, we refuse to
hand it to the aggregator.

Rules enforced (see templates/review-personas/README.md § 3 and § 3.2):

  1. Output must be **raw YAML** -- no Markdown code fences (```yaml)
     surrounding it, no natural-language preamble or trailer.
  2. Must parse as a YAML mapping.
  3. Must contain all required top-level keys:
       persona, verdict, summary, findings, followups, escalate_to_human
  4. `verdict` must be one of:
       abstain | approve | approve-with-changes | request-changes | block
  5. If `--persona <name>` is passed, the `persona` field must match it.
  6. `findings` must be a list (possibly empty).
  7. `escalate_to_human` must be a mapping with `required` (bool) and
     `reason` (string).

Exit code 0 on success; 1 on any violation.  Prints human-readable
diagnostics to stderr.

Usage:
  python3 scripts/validate_persona_output.py --input path/to/review.yaml
  python3 scripts/validate_persona_output.py --persona security --input ...
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml  # type: ignore[import-not-found]
except ImportError:
    yaml = None  # type: ignore[assignment]

VALID_VERDICTS = {
    "abstain",
    "approve",
    "approve-with-changes",
    "request-changes",
    "block",
}

REQUIRED_TOP_LEVEL = {
    "persona",
    "verdict",
    "summary",
    "findings",
    "followups",
    "escalate_to_human",
}

# A YAML document fenced as ```yaml ... ``` (or just ``` ... ```).
FENCE_OPEN_RE = re.compile(r"^\s*```")


def check_no_fence(raw: str) -> list[str]:
    errors: list[str] = []
    # First non-blank line must not start a code fence.
    first_nonblank = ""
    for line in raw.splitlines():
        if line.strip():
            first_nonblank = line.rstrip()
            break
    if FENCE_OPEN_RE.match(first_nonblank):
        errors.append(
            "output starts with a Markdown code fence (```). "
            "Adapters must emit raw YAML to stdout, not a fenced block. "
            "See templates/review-personas/README.md § 3.2."
        )
    # A closing fence anywhere alone on a line is also suspicious.
    for idx, line in enumerate(raw.splitlines(), 1):
        stripped = line.strip()
        if stripped in {"```", "```yaml", "```yml"}:
            errors.append(f"line {idx}: stray Markdown code fence '{stripped}'")
            break  # one message is enough
    return errors


def check_schema(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level YAML must be a mapping"]
    missing = REQUIRED_TOP_LEVEL - set(data.keys())
    if missing:
        errors.append(
            "missing required keys: " + ", ".join(sorted(missing))
        )
    verdict = data.get("verdict")
    if verdict is not None and verdict not in VALID_VERDICTS:
        errors.append(
            f"verdict={verdict!r} not in "
            + str(sorted(VALID_VERDICTS))
        )
    findings = data.get("findings")
    if findings is not None and not isinstance(findings, list):
        errors.append("findings must be a list (use [] when empty, not null)")
    followups = data.get("followups")
    if followups is not None and not isinstance(followups, list):
        errors.append("followups must be a list")
    esc = data.get("escalate_to_human")
    if esc is not None:
        if not isinstance(esc, dict):
            errors.append("escalate_to_human must be a mapping with `required` and `reason`")
        else:
            if "required" not in esc:
                errors.append("escalate_to_human.required missing")
            if "reason" not in esc:
                errors.append("escalate_to_human.reason missing")
            if not isinstance(esc.get("required", False), bool):
                errors.append("escalate_to_human.required must be a boolean")
    return errors


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument(
        "--persona",
        type=str,
        default=None,
        help="expected persona name; if set, the file's `persona` field must match",
    )
    args = ap.parse_args(argv[1:])

    if yaml is None:
        print(
            "validate_persona_output: pyyaml missing; cannot validate. "
            "Install pyyaml>=6.0 (CI does this). Skipping.",
            file=sys.stderr,
        )
        return 0

    raw = args.input.read_text(encoding="utf-8")

    errors: list[str] = []
    errors.extend(check_no_fence(raw))

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        print(f"YAML parse error: {exc}", file=sys.stderr)
        return 1

    errors.extend(check_schema(data))

    # Cross-check persona field vs expectation, if given.
    if args.persona and isinstance(data, dict):
        got = data.get("persona")
        if got != args.persona:
            errors.append(
                f"persona field is {got!r} but invoker expected {args.persona!r}"
            )

    if errors:
        print(
            f"validate_persona_output: {args.input} failed validation:",
            file=sys.stderr,
        )
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
