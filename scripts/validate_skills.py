#!/usr/bin/env python3
"""Validate toolkit skill and agent markdown frontmatter."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATTERNS = ("skills/*/SKILL.md", "agents/*.md", "agents/**/*.md")
REQUIRED_KEYS = ("name", "description")
KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(.*)$")
BLOCK_SCALARS = {"|", "|-", "|+", ">", ">-", ">+"}
DESCRIPTION_LIMIT = 250


@dataclass
class ValidationIssue:
    line: int
    message: str
    severity: str = "error"


class FrontmatterError(Exception):
    def __init__(self, line: int, message: str) -> None:
        super().__init__(message)
        self.line = line
        self.message = message


def resolve_targets(raw_paths: list[str]) -> list[Path]:
    if raw_paths:
        targets: list[Path] = []
        seen: set[Path] = set()
        for raw_path in raw_paths:
            path = Path(raw_path)
            if not path.is_absolute():
                path = ROOT / path
            resolved = path.resolve()
            if resolved not in seen:
                targets.append(resolved)
                seen.add(resolved)
        return targets

    targets = []
    seen = set()
    for pattern in DEFAULT_PATTERNS:
        for path in sorted(ROOT.glob(pattern)):
            resolved = path.resolve()
            if resolved not in seen and resolved.is_file():
                targets.append(resolved)
                seen.add(resolved)
    return targets


def split_frontmatter(text: str) -> tuple[list[str], int]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FrontmatterError(1, "missing YAML frontmatter delimited by ---")

    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return lines[1:idx], idx + 1

    raise FrontmatterError(1, "missing closing YAML frontmatter delimiter ---")


def fold_lines(lines: list[str]) -> str:
    parts: list[str] = []
    paragraph_break = False

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            paragraph_break = True
            continue
        if parts:
            parts.append("\n\n" if paragraph_break else " ")
        parts.append(stripped)
        paragraph_break = False

    return "".join(parts).strip()


def normalize_value(initial: str, continuations: list[str], line_number: int) -> str:
    if initial in BLOCK_SCALARS:
        if initial.startswith(">"):
            return fold_lines(continuations)
        return "\n".join(line.rstrip() for line in continuations).strip()

    if not initial:
        return fold_lines(continuations)

    if continuations:
        raise FrontmatterError(
            line_number,
            "unexpected indented continuation for a scalar value; use `>-` or put the value on the same line",
        )

    return initial.strip()


def parse_frontmatter(frontmatter_lines: list[str]) -> dict[str, str]:
    if not frontmatter_lines:
        raise FrontmatterError(1, "frontmatter block is empty")

    entries: list[tuple[str, str, list[str], int]] = []
    current_key: str | None = None
    current_initial = ""
    current_continuations: list[str] = []
    current_line = 2

    def flush_current() -> None:
        nonlocal current_key, current_initial, current_continuations, current_line
        if current_key is None:
            return
        entries.append((current_key, current_initial, current_continuations[:], current_line))
        current_key = None
        current_initial = ""
        current_continuations = []
        current_line = 2

    for offset, raw_line in enumerate(frontmatter_lines, start=2):
        if raw_line.startswith((" ", "\t")):
            if current_key is None:
                raise FrontmatterError(offset, "unexpected indented line before any frontmatter key")
            current_continuations.append(raw_line.lstrip())
            continue

        if not raw_line.strip():
            if current_key is not None:
                current_continuations.append("")
            continue

        match = KEY_RE.match(raw_line)
        if not match:
            raise FrontmatterError(offset, f"invalid frontmatter line: {raw_line}")

        flush_current()
        current_key = match.group(1)
        current_initial = match.group(2).strip()
        current_line = offset

    flush_current()

    parsed: dict[str, str] = {}
    for key, initial, continuations, line_number in entries:
        if key in parsed:
            raise FrontmatterError(line_number, f"duplicate frontmatter key: {key}")
        parsed[key] = normalize_value(initial, continuations, line_number)

    return parsed


def validate_file(path: Path) -> list[ValidationIssue]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [ValidationIssue(1, f"could not read file: {exc}")]

    try:
        frontmatter_lines, _closing_line = split_frontmatter(text)
        frontmatter = parse_frontmatter(frontmatter_lines)
    except FrontmatterError as exc:
        return [ValidationIssue(exc.line, exc.message)]

    issues: list[ValidationIssue] = []
    for key in REQUIRED_KEYS:
        value = frontmatter.get(key, "").strip()
        if not value:
            issues.append(ValidationIssue(1, f"missing required frontmatter key: {key}"))

    description = " ".join(frontmatter.get("description", "").split())
    if description and len(description) > DESCRIPTION_LIMIT:
        issues.append(
            ValidationIssue(
                1,
                f"description is {len(description)} chars; keep it at or under {DESCRIPTION_LIMIT}",
                severity="warning",
            )
        )

    return issues


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate SKILL.md and agent frontmatter in this repo."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional file paths to validate. Defaults to all skills and agents.",
    )
    args = parser.parse_args()

    targets = resolve_targets(args.paths)
    if not targets:
        print("No skill or agent markdown files matched.", file=sys.stderr)
        return 1

    error_count = 0
    warning_count = 0
    for path in targets:
        issues = validate_file(path)
        if not issues:
            continue
        for issue in issues:
            stream = sys.stderr if issue.severity == "error" else sys.stdout
            print(
                f"{display_path(path)}:{issue.line}: {issue.severity}: {issue.message}",
                file=stream,
            )
            if issue.severity == "error":
                error_count += 1
            else:
                warning_count += 1

    if error_count:
        return 1

    summary = f"Validated {len(targets)} file(s)."
    if warning_count:
        summary = f"{summary} {warning_count} warning(s)."
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
