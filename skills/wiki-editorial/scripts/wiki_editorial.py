#!/usr/bin/env python3
"""Scaffold, publish, and lint toolkit knowledge-wiki proposals."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_WIKI_ROOT = REPO_ROOT / "knowledge-wiki"
VALID_STATUS = {"fact", "hypothesis"}
VALID_CONFIDENCE = {"low", "medium", "high"}
VALID_REVIEW_BASIS = {"explicit_source", "self_report", "observed_behavior", "inference"}
STALE_AFTER_DAYS = {"fact": 180, "hypothesis": 90}
PLACEHOLDER_MARKERS = ("TBD", "{{", "TODO")


@dataclass
class Message:
    severity: str
    path: str
    text: str


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    wiki_root = Path(args.wiki_root).expanduser().resolve()
    ensure_wiki_root(wiki_root)

    if args.command == "propose":
        return cmd_propose(args, wiki_root)
    if args.command == "publish":
        return cmd_publish(args, wiki_root)
    if args.command == "lint":
        return cmd_lint(args, wiki_root)

    parser.error(f"unknown command: {args.command}")
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-root", default=str(DEFAULT_WIKI_ROOT), help="Path to the knowledge-wiki root")
    subparsers = parser.add_subparsers(dest="command", required=True)

    propose = subparsers.add_parser("propose", help="Copy explicit sources and scaffold candidate artifacts")
    propose.add_argument("--title", required=True, help="Human-readable proposal title")
    propose.add_argument("--domain", required=True, help="Canonical domain label")
    propose.add_argument("--status", choices=sorted(VALID_STATUS), required=True, help="Default page status")
    propose.add_argument(
        "--review-basis",
        choices=sorted(VALID_REVIEW_BASIS),
        required=True,
        help="Basis for the proposed canonical claims",
    )
    propose.add_argument(
        "--source",
        action="append",
        required=True,
        help="Absolute or relative path to a source file to copy into raw/ingest",
    )
    propose.add_argument(
        "--target-path",
        action="append",
        required=True,
        help="Canonical target path, e.g. canonical/preferences/communication-style.md",
    )
    propose.add_argument(
        "--neighbor-path",
        action="append",
        default=[],
        help="Impacted canonical neighbor path to re-review during the cycle",
    )

    publish = subparsers.add_parser("publish", help="Publish an approved proposal into canonical")
    publish.add_argument("--proposal-id", required=True, help="Proposal id from a prior propose cycle")

    lint = subparsers.add_parser("lint", help="Lint canonical pages or a staged proposal")
    scope = lint.add_mutually_exclusive_group(required=True)
    scope.add_argument("--proposal-id", help="Lint touched pages and neighbors for a staged proposal")
    scope.add_argument("--full", action="store_true", help="Lint the entire canonical corpus")
    return parser


def ensure_wiki_root(wiki_root: Path) -> None:
    required_dirs = [
        wiki_root / "raw" / "ingest",
        wiki_root / "candidate" / "reports",
        wiki_root / "candidate" / "patches",
        wiki_root / "canonical",
        wiki_root / "system",
    ]
    for path in required_dirs:
        path.mkdir(parents=True, exist_ok=True)


def cmd_propose(args: argparse.Namespace, wiki_root: Path) -> int:
    target_paths = [normalize_target_path(path) for path in args.target_path]
    if len(target_paths) > 2:
        die("A proposal may target at most two canonical pages.")

    neighbor_paths = [normalize_target_path(path) for path in args.neighbor_path]
    if args.review_basis == "inference" and args.status != "hypothesis":
        die("review-basis inference must use status hypothesis.")

    proposal_id = build_proposal_id(args.title)
    raw_dir = wiki_root / "raw" / "ingest" / proposal_id
    if raw_dir.exists():
        die(f"Proposal already exists: {proposal_id}")
    raw_dir.mkdir(parents=True)

    source_refs = copy_sources(args.source, raw_dir, wiki_root)
    write_manifest(raw_dir, proposal_id, args.title, source_refs, args.source)

    report_path = wiki_root / "candidate" / "reports" / f"{proposal_id}.md"
    patch_path = wiki_root / "candidate" / "patches" / f"{proposal_id}.md"
    report_path.write_text(
        render_report_template(
            proposal_id=proposal_id,
            title=args.title,
            status=args.status,
            domain=args.domain,
            review_basis=args.review_basis,
            source_refs=source_refs,
            target_paths=target_paths,
            neighbor_paths=neighbor_paths,
        ),
        encoding="utf-8",
    )
    patch_path.write_text(
        render_patch_template(
            wiki_root=wiki_root,
            proposal_id=proposal_id,
            title=args.title,
            status=args.status,
            domain=args.domain,
            review_basis=args.review_basis,
            source_refs=source_refs,
            target_paths=target_paths,
        ),
        encoding="utf-8",
    )

    print(f"proposal_id: {proposal_id}")
    print(f"raw_dir: {raw_dir.relative_to(wiki_root)}")
    print(f"report: {report_path.relative_to(wiki_root)}")
    print(f"patch: {patch_path.relative_to(wiki_root)}")
    return 0


def cmd_publish(args: argparse.Namespace, wiki_root: Path) -> int:
    proposal_id = args.proposal_id
    report_meta, _report_body, patch_meta, patch_targets = load_candidate_files(wiki_root, proposal_id)
    if report_meta.get("recommendation") != "approve":
        die("Candidate report recommendation must be set to `approve` before publish.")
    target_paths = [normalize_target_path(path) for path in patch_meta.get("target_paths", [])]
    if sorted(target_paths) != sorted(patch_targets.keys()):
        die("Candidate patch target_paths frontmatter does not match target blocks.")
    report_target_paths = [normalize_target_path(path) for path in report_meta.get("target_paths", [])]
    if sorted(report_target_paths) != sorted(target_paths):
        die("Candidate report target_paths must match the patch targets.")

    current_pages = load_canonical_pages(wiki_root)
    staged_pages = dict(current_pages)
    staged_pages.update(patch_targets)

    scope_paths = compute_local_scope(
        report_meta.get("target_paths", []),
        report_meta.get("neighbor_paths", []),
        current_pages,
        staged_pages,
    )
    messages = lint_pages(scope_paths, staged_pages, wiki_root, include_global_checks=False)
    error_count = sum(1 for msg in messages if msg.severity == "ERROR")
    warning_count = sum(1 for msg in messages if msg.severity == "WARNING")
    if error_count:
        print_messages(messages)
        die("Publish blocked by local lint errors.", code=1)

    for rel_path, content in patch_targets.items():
        destination = wiki_root / rel_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    updated_pages = load_canonical_pages(wiki_root)
    index_path = wiki_root / "system" / "index.md"
    index_path.write_text(render_index(updated_pages), encoding="utf-8")

    log_path = wiki_root / "system" / "log.md"
    append_log_entry(
        log_path=log_path,
        report_meta=report_meta,
        proposal_id=proposal_id,
        warning_count=warning_count,
    )

    print(f"published: {', '.join(sorted(patch_targets))}")
    print(f"index: {index_path.relative_to(wiki_root)}")
    print(f"log: {log_path.relative_to(wiki_root)}")
    if warning_count:
        print_messages(messages)
    return 0


def cmd_lint(args: argparse.Namespace, wiki_root: Path) -> int:
    if args.full:
        pages = load_canonical_pages(wiki_root)
        messages = lint_pages(sorted(pages), pages, wiki_root, include_global_checks=True)
    else:
        report_meta, _report_body, _patch_meta, patch_targets = load_candidate_files(wiki_root, args.proposal_id)
        current_pages = load_canonical_pages(wiki_root)
        staged_pages = dict(current_pages)
        staged_pages.update(patch_targets)
        scope_paths = compute_local_scope(
            report_meta.get("target_paths", []),
            report_meta.get("neighbor_paths", []),
            current_pages,
            staged_pages,
        )
        messages = lint_pages(scope_paths, staged_pages, wiki_root, include_global_checks=False)

    print_messages(messages)
    return 1 if any(msg.severity == "ERROR" for msg in messages) else 0


def copy_sources(source_args: list[str], raw_dir: Path, wiki_root: Path) -> list[str]:
    source_refs: list[str] = []
    for index, source_arg in enumerate(source_args, start=1):
        source_path = Path(source_arg).expanduser().resolve()
        if not source_path.exists() or not source_path.is_file():
            die(f"Source file not found: {source_arg}")
        destination_name = f"source-{index:02d}-{sanitize_filename(source_path.name)}"
        destination = raw_dir / destination_name
        shutil.copy2(source_path, destination)
        source_refs.append(rel_to(destination, wiki_root))
    return source_refs


def write_manifest(
    raw_dir: Path, proposal_id: str, title: str, source_refs: list[str], source_args: list[str]
) -> None:
    manifest = {
        "proposal_id": proposal_id,
        "title": title,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sources": [],
    }
    for copied_ref, original in zip(source_refs, source_args, strict=True):
        copied_path = raw_dir.parents[2] / copied_ref
        manifest["sources"].append(
            {
                "original_path": str(Path(original).expanduser().resolve()),
                "copied_path": copied_ref,
                "sha256": sha256(copied_path),
            }
        )
    (raw_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def load_candidate_files(wiki_root: Path, proposal_id: str) -> tuple[dict, str, dict, dict[str, str]]:
    report_path = wiki_root / "candidate" / "reports" / f"{proposal_id}.md"
    patch_path = wiki_root / "candidate" / "patches" / f"{proposal_id}.md"
    if not report_path.exists():
        die(f"Missing candidate report: {report_path}")
    if not patch_path.exists():
        die(f"Missing candidate patch: {patch_path}")

    report_meta, report_body = parse_frontmatter(report_path.read_text(encoding="utf-8"))
    patch_meta, patch_body = parse_frontmatter(patch_path.read_text(encoding="utf-8"))
    patch_targets = parse_patch_targets(patch_body)
    if len(patch_targets) > 2:
        die("A candidate patch may target at most two canonical pages.")
    return report_meta, report_body, patch_meta, patch_targets


def load_canonical_pages(wiki_root: Path) -> dict[str, str]:
    pages: dict[str, str] = {}
    canonical_root = wiki_root / "canonical"
    for path in sorted(canonical_root.rglob("*.md")):
        if path.name == ".gitkeep":
            continue
        pages[rel_to(path, wiki_root)] = path.read_text(encoding="utf-8")
    return pages


def render_report_template(
    *,
    proposal_id: str,
    title: str,
    status: str,
    domain: str,
    review_basis: str,
    source_refs: list[str],
    target_paths: list[str],
    neighbor_paths: list[str],
) -> str:
    lines = [
        "---",
        f"proposal_id: {proposal_id}",
        f"title: {title}",
        f"status: {status}",
        f"domain: {domain}",
        f"review_basis: {review_basis}",
        "recommendation: pending",
        "source_refs:",
    ]
    lines.extend(f"  - {ref}" for ref in source_refs)
    lines.append("target_paths:")
    lines.extend(f"  - {path}" for path in target_paths)
    if neighbor_paths:
        lines.append("neighbor_paths:")
        lines.extend(f"  - {path}" for path in neighbor_paths)
    else:
        lines.append("neighbor_paths: []")
    lines.extend(
        [
            "---",
            f"# Candidate Report: {title}",
            "",
            "## Why this deserves canon",
            "TBD",
            "",
            "## Proposed changes",
            "TBD",
            "",
            "## Impacted existing pages",
            "TBD",
            "",
            "## Uncertainty and contradictions",
            "TBD",
            "",
            "## Publication recommendation",
            "Set `recommendation` in frontmatter to `approve` or `reject` after review.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_patch_template(
    *,
    wiki_root: Path,
    proposal_id: str,
    title: str,
    status: str,
    domain: str,
    review_basis: str,
    source_refs: list[str],
    target_paths: list[str],
) -> str:
    lines = [
        "---",
        f"proposal_id: {proposal_id}",
        f"title: {title}",
        "target_paths:",
    ]
    lines.extend(f"  - {path}" for path in target_paths)
    lines.extend(["---", f"# Candidate Patch: {title}", "", "Replace each fenced block with the full file content to publish.", ""])
    for target_path in target_paths:
        current_path = wiki_root / target_path
        if current_path.exists():
            file_body = current_path.read_text(encoding="utf-8").rstrip()
        else:
            file_body = canonical_template(
                title=humanize_slug(Path(target_path).stem),
                status=status,
                domain=domain,
                review_basis=review_basis,
                source_refs=source_refs,
            ).rstrip()
        lines.extend([f"## Target: {target_path}", "```md", file_body, "```", ""])
    return "\n".join(lines).rstrip() + "\n"


def canonical_template(
    *, title: str, status: str, domain: str, review_basis: str, source_refs: list[str]
) -> str:
    lines = [
        "---",
        f"title: {title}",
        f"status: {status}",
        f"domain: {domain}",
        "confidence: medium",
        "source_refs:",
    ]
    lines.extend(f"  - {ref}" for ref in source_refs)
    lines.extend(
        [
            f"last_reviewed: {dt.date.today().isoformat()}",
            f"review_basis: {review_basis}",
            "contradicts: []",
            "supersedes: []",
            "---",
            f"# {title}",
            "",
            "## Claim",
            "TBD",
            "",
            "## Rationale",
            "TBD",
            "",
            "## Sources",
        ]
    )
    lines.extend(f"- `{ref}`" for ref in source_refs)
    return "\n".join(lines)


def parse_patch_targets(body: str) -> dict[str, str]:
    pattern = re.compile(r"^## Target: (?P<path>[^\n]+)\n```(?:md)?\n(?P<content>.*?)\n```", re.MULTILINE | re.DOTALL)
    targets: dict[str, str] = {}
    for match in pattern.finditer(body):
        target_path = normalize_target_path(match.group("path").strip())
        targets[target_path] = match.group("content").rstrip() + "\n"
    if not targets:
        die("Candidate patch does not contain any `## Target:` blocks.")
    return targets


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        die("Expected YAML frontmatter starting with `---`.")
    end = text.find("\n---\n", 4)
    if end == -1:
        die("Could not find closing frontmatter marker.")
    raw_meta = text[4:end]
    body = text[end + 5 :]
    return parse_simple_yaml(raw_meta), body


def parse_simple_yaml(text: str) -> dict:
    data: dict[str, object] = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if ":" not in line:
            die(f"Invalid frontmatter line: {line}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not raw_value:
            items: list[object] = []
            index += 1
            while index < len(lines):
                nested = lines[index]
                if not nested.strip():
                    index += 1
                    continue
                if nested.startswith("  - "):
                    items.append(parse_scalar(nested[4:].strip()))
                    index += 1
                    continue
                break
            data[key] = items
            continue
        data[key] = parse_scalar(raw_value)
        index += 1
    return data


def parse_scalar(raw: str) -> object:
    if raw in {"[]", "{}"}:
        return [] if raw == "[]" else {}
    if raw.startswith("[") or raw.startswith("{"):
        return json.loads(raw)
    return raw


def lint_pages(
    scope_paths: Iterable[str], pages: dict[str, str], wiki_root: Path, *, include_global_checks: bool
) -> list[Message]:
    messages: list[Message] = []
    scope = sorted(set(normalize_target_path(path) for path in scope_paths if path))
    titles: dict[str, list[str]] = {}
    graph = build_link_graph(pages)

    for rel_path, text in pages.items():
        meta, _body = parse_frontmatter(text)
        title = str(meta.get("title", "")).strip().lower()
        if title:
            titles.setdefault(title, []).append(rel_path)

    for rel_path in scope:
        if rel_path not in pages:
            messages.append(Message("ERROR", rel_path, "Referenced page does not exist in the staged canonical set."))
            continue
        meta, body = parse_frontmatter(pages[rel_path])
        messages.extend(validate_page(rel_path, meta, body, wiki_root, pages))

    if include_global_checks:
        for title, paths in sorted(titles.items()):
            if len(paths) > 1:
                for rel_path in paths:
                    messages.append(Message("WARNING", rel_path, f"Duplicate canonical title: {title}"))

        inbound = reverse_graph(graph)
        for rel_path in sorted(pages):
            outgoing = graph.get(rel_path, set())
            if not outgoing and not inbound.get(rel_path):
                messages.append(Message("WARNING", rel_path, "Canonical page is orphaned from the internal graph."))

        superseded_by = build_superseded_map(pages)
        for rel_path, newer_paths in superseded_by.items():
            messages.append(
                Message(
                    "WARNING",
                    rel_path,
                    "Page is marked as superseded by: " + ", ".join(sorted(newer_paths)),
                )
            )

    return sorted(messages, key=lambda item: (item.severity != "ERROR", item.path, item.text))


def validate_page(rel_path: str, meta: dict, body: str, wiki_root: Path, pages: dict[str, str]) -> list[Message]:
    messages: list[Message] = []
    required = [
        "title",
        "status",
        "domain",
        "confidence",
        "source_refs",
        "last_reviewed",
        "review_basis",
        "contradicts",
        "supersedes",
    ]
    for key in required:
        if key not in meta:
            messages.append(Message("ERROR", rel_path, f"Missing frontmatter field: {key}"))

    status = str(meta.get("status", ""))
    confidence = str(meta.get("confidence", ""))
    review_basis = str(meta.get("review_basis", ""))
    source_refs = meta.get("source_refs", [])
    contradicts = meta.get("contradicts", [])
    supersedes = meta.get("supersedes", [])

    if status and status not in VALID_STATUS:
        messages.append(Message("ERROR", rel_path, f"Invalid status: {status}"))
    if confidence and confidence not in VALID_CONFIDENCE:
        messages.append(Message("ERROR", rel_path, f"Invalid confidence: {confidence}"))
    if review_basis and review_basis not in VALID_REVIEW_BASIS:
        messages.append(Message("ERROR", rel_path, f"Invalid review_basis: {review_basis}"))
    if not isinstance(source_refs, list):
        messages.append(Message("ERROR", rel_path, "source_refs must be a list."))
        source_refs = []
    if not isinstance(contradicts, list):
        messages.append(Message("ERROR", rel_path, "contradicts must be a list."))
        contradicts = []
    if not isinstance(supersedes, list):
        messages.append(Message("ERROR", rel_path, "supersedes must be a list."))
        supersedes = []

    if review_basis == "inference" and status == "fact":
        messages.append(Message("ERROR", rel_path, "Inference-based pages must remain hypothesis until confirmed."))

    if not source_refs:
        messages.append(Message("ERROR", rel_path, "Canonical page must have at least one source_ref."))
    for source_ref in source_refs:
        source_path = wiki_root / str(source_ref)
        if not source_path.exists():
            messages.append(Message("ERROR", rel_path, f"Missing source_ref target: {source_ref}"))
        elif not str(source_ref).startswith("raw/ingest/"):
            messages.append(Message("ERROR", rel_path, f"source_ref must live under raw/ingest/: {source_ref}"))

    for field_name, refs in (("contradicts", contradicts), ("supersedes", supersedes)):
        for ref in refs:
            target = normalize_target_path(str(ref))
            if not target.startswith("canonical/"):
                messages.append(Message("ERROR", rel_path, f"{field_name} must point at canonical pages: {ref}"))
            elif target not in pages:
                messages.append(Message("ERROR", rel_path, f"{field_name} target does not exist: {ref}"))

    try:
        reviewed_on = dt.date.fromisoformat(str(meta.get("last_reviewed", "")))
    except ValueError:
        messages.append(Message("ERROR", rel_path, "last_reviewed must be an ISO date."))
        reviewed_on = None
    if reviewed_on and status in STALE_AFTER_DAYS:
        age = (dt.date.today() - reviewed_on).days
        if age > STALE_AFTER_DAYS[status]:
            messages.append(Message("WARNING", rel_path, f"Page review is stale ({age} days old)."))

    if confidence == "high" and len(source_refs) < 2:
        messages.append(Message("WARNING", rel_path, "High-confidence page has weak provenance (<2 sources)."))

    if any(marker in body for marker in PLACEHOLDER_MARKERS):
        messages.append(Message("ERROR", rel_path, "Published page still contains placeholder text."))

    for link_target in local_markdown_links(body, rel_path):
        if not link_target.endswith(".md"):
            continue
        normalized = normalize_relative_markdown_target(rel_path, link_target)
        if normalized and normalized not in pages and not (wiki_root / normalized).exists():
            messages.append(Message("ERROR", rel_path, f"Broken local markdown link: {link_target}"))

    return messages


def build_link_graph(pages: dict[str, str]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for rel_path, text in pages.items():
        graph[rel_path] = {
            target
            for target in (
                normalize_relative_markdown_target(rel_path, raw_target)
                for raw_target in local_markdown_links(parse_frontmatter(text)[1], rel_path)
            )
            if target and target in pages
        }
    return graph


def reverse_graph(graph: dict[str, set[str]]) -> dict[str, set[str]]:
    inbound: dict[str, set[str]] = {}
    for source, targets in graph.items():
        for target in targets:
            inbound.setdefault(target, set()).add(source)
    return inbound


def build_superseded_map(pages: dict[str, str]) -> dict[str, set[str]]:
    superseded_by: dict[str, set[str]] = {}
    for rel_path, text in pages.items():
        meta, _body = parse_frontmatter(text)
        for older in meta.get("supersedes", []):
            normalized = normalize_target_path(str(older))
            superseded_by.setdefault(normalized, set()).add(rel_path)
    return superseded_by


def compute_local_scope(
    target_paths: list[str], neighbor_paths: list[str], current_pages: dict[str, str], staged_pages: dict[str, str]
) -> list[str]:
    touched = {normalize_target_path(path) for path in target_paths}
    neighbors = {normalize_target_path(path) for path in neighbor_paths}
    graph = build_link_graph(staged_pages)
    inbound = reverse_graph(graph)
    scope = set()
    for rel_path in touched:
        scope.add(rel_path)
        scope.update(graph.get(rel_path, set()))
        scope.update(inbound.get(rel_path, set()))
    scope.update(path for path in neighbors if path in current_pages or path in staged_pages)
    return sorted(scope)


def render_index(pages: dict[str, str]) -> str:
    if not pages:
        return "# Canonical Index\n\n_Auto-generated by `wiki-editorial publish`. Do not hand-edit._\n\nNo canonical pages published yet.\n"

    grouped: dict[str, list[tuple[str, dict]]] = {}
    for rel_path, text in pages.items():
        meta, _body = parse_frontmatter(text)
        grouped.setdefault(str(meta["domain"]), []).append((rel_path, meta))

    lines = [
        "# Canonical Index",
        "",
        "_Auto-generated by `wiki-editorial publish`. Do not hand-edit._",
        "",
        f"Updated: {dt.datetime.now().astimezone().replace(microsecond=0).isoformat()}",
        "",
    ]
    for domain in sorted(grouped):
        lines.append(f"## {domain}")
        lines.append("")
        for rel_path, meta in sorted(grouped[domain], key=lambda item: str(item[1]["title"]).lower()):
            lines.append(
                "- "
                f"[{meta['title']}](../{rel_path})"
                f" · status: `{meta['status']}`"
                f" · confidence: `{meta['confidence']}`"
                f" · reviewed: `{meta['last_reviewed']}`"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def append_log_entry(log_path: Path, report_meta: dict, proposal_id: str, warning_count: int) -> None:
    timestamp = dt.datetime.now().astimezone().replace(microsecond=0).isoformat()
    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Publication Log\n"
    entry_lines = [
        "",
        f"## {timestamp} · {proposal_id}",
        "",
        f"- Title: {report_meta.get('title', proposal_id)}",
        f"- Targets: {', '.join(report_meta.get('target_paths', []))}",
        f"- Sources: {', '.join(report_meta.get('source_refs', []))}",
        f"- Neighbors reviewed: {', '.join(report_meta.get('neighbor_paths', []))}",
        f"- Recommendation at publish time: {report_meta.get('recommendation', 'unknown')}",
        f"- Lint warnings: {warning_count}",
    ]
    if existing.rstrip().endswith("No publications yet."):
        existing = existing.rstrip()[:-len("No publications yet.")] + "\n"
    log_path.write_text(existing.rstrip() + "\n" + "\n".join(entry_lines).rstrip() + "\n", encoding="utf-8")


def local_markdown_links(body: str, rel_path: str) -> list[str]:
    del rel_path
    return [
        link
        for link in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body)
        if not re.match(r"^[a-z]+://", link) and not link.startswith("#")
    ]


def normalize_relative_markdown_target(base_rel_path: str, raw_target: str) -> str | None:
    if raw_target.startswith(("mailto:", "http://", "https://")):
        return None
    target = raw_target.split("#", 1)[0]
    if not target:
        return None
    combined = PurePosixPath(base_rel_path).parent / PurePosixPath(target)
    normalized_parts: list[str] = []
    for part in combined.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not normalized_parts:
                return None
            normalized_parts.pop()
            continue
        normalized_parts.append(part)
    return "/".join(normalized_parts) if normalized_parts else None


def normalize_target_path(raw_path: str) -> str:
    path = raw_path.strip()
    if not path:
        die("Empty target path.")
    candidate = Path(path)
    if candidate.is_absolute():
        die(f"Target path must be relative to knowledge-wiki: {raw_path}")
    normalized = candidate.as_posix()
    if normalized.startswith("../") or "/../" in normalized or normalized == "..":
        die(f"Target path escapes the wiki root: {raw_path}")
    if not normalized.endswith(".md"):
        die(f"Target path must end in .md: {raw_path}")
    if not normalized.startswith("canonical/"):
        die(f"Target path must live under canonical/: {raw_path}")
    return normalized


def build_proposal_id(title: str) -> str:
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{slugify(title)}"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:48] or "proposal"


def humanize_slug(text: str) -> str:
    return re.sub(r"[-_]+", " ", text).strip().title() or "Untitled"


def sanitize_filename(name: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")
    return safe or "source"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel_to(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def print_messages(messages: list[Message]) -> None:
    if not messages:
        print("OK: no lint findings")
        return
    for message in messages:
        print(f"{message.severity}: {message.path}: {message.text}")


def die(message: str, code: int = 2) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


if __name__ == "__main__":
    raise SystemExit(main())
