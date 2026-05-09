#!/usr/bin/env python3
"""
Validate internal cross-references in markdown documentation.

We write lots of sentences like:
    See `AGENTS.md § 3.1`
    Per `.kiro/steering/security.md § 7`
    Refer to `templates/review-personas/README.md § 3.2`
These references are load-bearing for agents reading the repo. If we
rename or renumber a section, the references silently rot and agents
start reading rules that "point into the void".

This script scans every tracked *.md file for such references and
verifies that:
  (1) the referenced file exists inside the repo
  (2) the referenced "§ N" or "§ N.M" heading exists in that file

Reference patterns supported
----------------------------
  `some/file.md` § 3
  `some/file.md § 3.1`
  some/file.md § 3
  AGENTS.md § 3.1
  `AGENTS.md` § 3
  templates/review-personas/README.md § 3
  .kiro/steering/harness.md § 2 R4       -> parses as § 2 (R4 is a sub-marker)

Non-goals
---------
  - Does NOT validate external URLs (that's a separate link-check job).
  - Does NOT validate anchors by slug (we use the literal § N prefix).
  - Conservative: prefers false negatives over false positives so that
    legitimate prose like "2 § 3 test cases" is not misread.

Usage
-----
  check_cross_refs.py                 # scan whole repo
  check_cross_refs.py file1 file2 ... # pre-commit mode: scan passed files
                                      # but resolve refs against repo root

Exit codes: 0 = clean, 1 = broken refs found, 2 = bad args.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# Section headings look like "## 3. Foo" / "### 3.1 Bar" / "### 3.1. Bar"
# Note: we accept the number even when followed by a period+space OR a space.
HEADING_RE = re.compile(
    r"^(?P<hashes>#{2,4})\s+(?P<num>\d+(?:\.\d+)*)(?:\.|(?=\s))",
    re.MULTILINE,
)

# A reference: `<path>.md` [backticks optional] § N[.M]
# We require the path to look like a markdown file with either a dot-slash
# or at least one slash OR a known top-level sentinel (AGENTS.md, README.md).
# This is intentional: bare "foo.md" would give too many false positives.
REF_RE = re.compile(
    r"""
    `?                                    # optional opening backtick
    (?P<path>
        (?:
            AGENTS\.md |                  # repo-root files we accept
            README\.md |
            CONTRIBUTING\.md |
            SECURITY\.md |
            CODE_OF_CONDUCT\.md |
            CODEOWNERS |
            LICENSE |
            [\w\-./]+/[\w\-./]+\.md       # any path-like markdown
        )
    )
    `?\s*§\s*                             # backtick optional, then §
    (?P<sec>\d+(?:\.\d+)*)                # 3 or 3.1 or 3.1.2
    """,
    re.VERBOSE,
)

# Exclude our own source (this script and test fixtures).
EXCLUDE_PATHS = {
    "scripts/check_cross_refs.py",
}


def find_markdown_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)


def extract_headings(md_path: Path) -> set[str]:
    """Return the set of 'N' / 'N.M' numeric section IDs declared in a file."""
    try:
        text = md_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    return {m.group("num") for m in HEADING_RE.finditer(text)}


def resolve_ref_path(ref_path: str, repo_root: Path, from_file: Path) -> Path | None:
    """
    Resolve a reference path against, in priority order:
      1. Sibling directory (from_file.parent / ref_path) -- common inside
         templates/review-personas/ where persona files refer to README.md
      2. Repo root (the most common explicit path, e.g. 'AGENTS.md')
      3. Any ancestor directory of from_file (one level up at a time) --
         handles cases like 'review-personas/README.md' written inside
         templates/review-personas/foo.md (intended relative, missing
         'templates/' prefix)
    Return the first existing hit, or None.
    """
    candidates: list[Path] = [
        from_file.parent / ref_path,
        repo_root / ref_path,
    ]
    # Walk up the tree from the file's directory toward the repo root
    # and try joining at each level. Stop before leaving the repo.
    here = from_file.parent
    try:
        here_rel = here.relative_to(repo_root)
    except ValueError:
        here_rel = None
    if here_rel is not None:
        for parent in here.parents:
            if parent == repo_root.parent:
                break
            candidates.append(parent / ref_path)
            if parent == repo_root:
                break

    for c in candidates:
        # Ensure resolved path stays inside the repo (no .. tricks).
        try:
            c_resolved = c.resolve()
            c_resolved.relative_to(repo_root)
        except (OSError, ValueError):
            continue
        if c_resolved.is_file():
            return c_resolved
    return None


def scan_file(
    md_path: Path, repo_root: Path, heading_cache: dict[Path, set[str]]
) -> list[str]:
    try:
        text = md_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [f"{md_path}: cannot read ({exc})"]

    errors: list[str] = []
    for m in REF_RE.finditer(text):
        ref_path = m.group("path")
        ref_sec = m.group("sec")

        target = resolve_ref_path(ref_path, repo_root, md_path)
        if target is None:
            # File doesn't exist in repo.
            errors.append(
                f"{md_path.relative_to(repo_root)}: reference to "
                f"non-existent file `{ref_path}` § {ref_sec}"
            )
            continue

        # Markdown file exists; check for the section.
        if target not in heading_cache:
            heading_cache[target] = extract_headings(target)
        if ref_sec not in heading_cache[target]:
            rel_target = target.relative_to(repo_root)
            errors.append(
                f"{md_path.relative_to(repo_root)}: references "
                f"`{rel_target}` § {ref_sec} which does not exist "
                f"(target has §: {sorted(heading_cache[target]) or 'none'})"
            )
    return errors


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "files",
        nargs="*",
        help="markdown files to scan; default: all *.md in repo",
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="repo root (default: cwd)",
    )
    args = ap.parse_args(argv[1:])

    repo_root = args.root.resolve()

    if args.files:
        targets = [Path(f).resolve() for f in args.files]
    else:
        targets = find_markdown_files(repo_root)

    heading_cache: dict[Path, set[str]] = {}

    rc = 0
    for p in targets:
        # Skip excluded files.
        try:
            rel = p.relative_to(repo_root).as_posix()
        except ValueError:
            rel = p.as_posix()
        if rel in EXCLUDE_PATHS:
            continue
        errs = scan_file(p, repo_root, heading_cache)
        for e in errs:
            print(e)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
