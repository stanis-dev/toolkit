#!/usr/bin/env python3
"""Prepare, assert, and aggregate declarative knowledge-wiki smoke scenarios."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = REPO_ROOT / "skills" / "wiki-editorial" / "smoke-fixtures"
DEFAULT_CATALOG = FIXTURE_ROOT / "catalog.json"
DEFAULT_CLI_PATH = REPO_ROOT / "skills" / "wiki-editorial" / "scripts" / "wiki_editorial.py"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    catalog = load_catalog(Path(args.catalog).resolve())

    if args.command == "list":
        return cmd_list(args, catalog)
    if args.command == "describe":
        return cmd_describe(args, catalog)
    if args.command == "prepare":
        return cmd_prepare(args, catalog)
    if args.command == "assert":
        return cmd_assert(args)
    if args.command == "aggregate":
        return cmd_aggregate(args)

    parser.error(f"unknown command: {args.command}")
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", default=str(DEFAULT_CATALOG), help="Path to the smoke scenario catalog")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List scenario batches and ids")
    list_parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text")

    describe = subparsers.add_parser("describe", help="Describe one scenario from the catalog")
    describe.add_argument("--scenario-id", required=True)

    prepare = subparsers.add_parser("prepare", help="Create an isolated workspace for one scenario")
    prepare.add_argument("--scenario-id", required=True)
    prepare.add_argument("--workspace-root", required=True)

    assert_parser = subparsers.add_parser("assert", help="Evaluate one prepared scenario after command execution")
    assert_parser.add_argument("--workspace-root", required=True)
    assert_parser.add_argument("--exit-code", required=True, type=int)
    assert_parser.add_argument("--stdout-file", required=True)
    assert_parser.add_argument("--stderr-file", required=True)
    assert_parser.add_argument("--output-file", help="Optional path to write the JSON verdict")

    aggregate = subparsers.add_parser("aggregate", help="Aggregate worker result JSON files into a release report")
    aggregate.add_argument("--result-file", action="append", required=True, help="Path to one result.json file")
    aggregate.add_argument("--json", action="store_true", help="Emit JSON only")
    return parser


def load_catalog(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def scenarios_by_id(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {scenario["id"]: scenario for scenario in catalog["scenarios"]}


def cmd_list(args: argparse.Namespace, catalog: dict[str, Any]) -> int:
    if args.json:
        print(json.dumps(catalog["batches"], indent=2))
        return 0

    for batch in catalog["batches"]:
        print(f"{batch['id']}:")
        for scenario_id in batch["scenario_ids"]:
            print(f"  - {scenario_id}")
    return 0


def cmd_describe(args: argparse.Namespace, catalog: dict[str, Any]) -> int:
    scenario = scenarios_by_id(catalog)[args.scenario_id]
    print(json.dumps(scenario, indent=2))
    return 0


def cmd_prepare(args: argparse.Namespace, catalog: dict[str, Any]) -> int:
    scenario = scenarios_by_id(catalog)[args.scenario_id]
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    if workspace_root.exists() and any(workspace_root.iterdir()):
        die(f"workspace root must be empty or absent: {workspace_root}")

    workspace_root.mkdir(parents=True, exist_ok=True)
    wiki_root = workspace_root / "wiki"
    artifacts_dir = workspace_root / "artifacts"
    ensure_wiki_dirs(wiki_root)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    seed_id = scenario.get("seed")
    if seed_id:
        copy_tree_contents(FIXTURE_ROOT / "seeds" / seed_id, wiki_root)

    context = {
        "repo_root": str(REPO_ROOT),
        "fixture_root": str(FIXTURE_ROOT),
        "workspace_root": str(workspace_root),
        "wiki_root": str(wiki_root),
        "artifacts_dir": str(artifacts_dir),
        "cli_path": str(DEFAULT_CLI_PATH),
        "hook_path": str(REPO_ROOT / "hooks" / "session-start.sh"),
    }

    apply_setup_steps(scenario.get("setup_steps", []), context)

    watch_hashes = {}
    for rel_path in scenario.get("watch_repo_paths", []):
        watch_hashes[rel_path] = hash_optional(REPO_ROOT / rel_path)

    prepared = {
        "scenario_id": scenario["id"],
        "batch": scenario["batch"],
        "gate": scenario["gate"],
        "workspace_root": str(workspace_root),
        "wiki_root": str(wiki_root),
        "cli_path": str(DEFAULT_CLI_PATH),
        "fixture_root": str(FIXTURE_ROOT),
        "setup_steps": scenario.get("setup_steps", []),
        "command": resolve_value(scenario["command"], context),
        "expected_exit": scenario["expected_exit"],
        "expected_stdout": scenario.get("expected_stdout", []),
        "expected_stderr": scenario.get("expected_stderr", []),
        "expected_files": scenario.get("expected_files", []),
        "expected_warnings": scenario.get("expected_warnings", []),
        "forbidden_paths": scenario.get("forbidden_paths", []),
        "captures": scenario.get("captures", []),
        "watch_repo_paths": scenario.get("watch_repo_paths", []),
        "watch_hashes": watch_hashes,
        "stdout_file": str(artifacts_dir / "stdout.txt"),
        "stderr_file": str(artifacts_dir / "stderr.txt"),
        "result_file": str(artifacts_dir / "result.json"),
        "scenario": scenario,
    }

    run_path = workspace_root / "run.json"
    run_path.write_text(json.dumps(prepared, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(prepared, indent=2))
    return 0


def cmd_assert(args: argparse.Namespace) -> int:
    workspace_root = Path(args.workspace_root).expanduser().resolve()
    run = json.loads((workspace_root / "run.json").read_text(encoding="utf-8"))
    stdout_path = Path(args.stdout_file).expanduser().resolve()
    stderr_path = Path(args.stderr_file).expanduser().resolve()
    stdout_text = stdout_path.read_text(encoding="utf-8") if stdout_path.exists() else ""
    stderr_text = stderr_path.read_text(encoding="utf-8") if stderr_path.exists() else ""
    combined = "\n".join(part for part in (stdout_text, stderr_text) if part)

    context = {
        "repo_root": str(REPO_ROOT),
        "fixture_root": run["fixture_root"],
        "workspace_root": run["workspace_root"],
        "wiki_root": run["wiki_root"],
        "artifacts_dir": str(Path(run["stdout_file"]).resolve().parent),
        "cli_path": run["cli_path"],
        "hook_path": str(REPO_ROOT / "hooks" / "session-start.sh"),
    }
    context.update(extract_captures(run.get("captures", []), stdout_text, stderr_text))

    assertions: list[dict[str, Any]] = []
    record_exit_assertion(run["expected_exit"], args.exit_code, assertions)
    evaluate_output_expectations("stdout", run.get("expected_stdout", []), stdout_text, context, assertions)
    evaluate_output_expectations("stderr", run.get("expected_stderr", []), stderr_text, context, assertions)
    warnings_seen = extract_lines(combined, "WARNING")
    errors_seen = extract_lines(combined, "ERROR")
    evaluate_warning_expectations(run.get("expected_warnings", []), combined, context, assertions)

    if run["expected_exit"] in {"success", "warning"}:
        if run["expected_exit"] == "success":
            assertions.append(
                assertion(
                    "no_warnings",
                    not warnings_seen,
                    "No warning lines emitted" if not warnings_seen else "Warnings emitted: " + "; ".join(warnings_seen),
                )
            )
        assertions.append(
            assertion(
                "no_errors",
                not errors_seen,
                "No error lines emitted" if not errors_seen else "Errors emitted: " + "; ".join(errors_seen),
            )
        )

    evaluate_file_expectations(run.get("expected_files", []), context, assertions)
    evaluate_forbidden_paths(run.get("forbidden_paths", []), context, assertions)
    evaluate_watch_paths(run.get("watch_repo_paths", []), run.get("watch_hashes", {}), assertions)

    verdict = "PASS" if all(item["pass"] for item in assertions) else "FAIL"
    result = {
        "scenario_id": run["scenario_id"],
        "batch": run["batch"],
        "gate": run["gate"],
        "verdict": verdict,
        "exit_code": args.exit_code,
        "assertions": assertions,
        "artifacts": {
            "workspace_root": run["workspace_root"],
            "stdout_file": str(stdout_path),
            "stderr_file": str(stderr_path),
            "result_file": run["result_file"],
        },
        "warnings_seen": warnings_seen,
        "errors_seen": errors_seen,
    }

    output_path = Path(args.output_file).expanduser().resolve() if args.output_file else Path(run["result_file"]).resolve()
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if verdict == "PASS" else 1


def cmd_aggregate(args: argparse.Namespace) -> int:
    results = [json.loads(Path(path).read_text(encoding="utf-8")) for path in args.result_file]
    total = len(results)
    pass_count = sum(1 for result in results if result["verdict"] == "PASS")
    fail_count = sum(1 for result in results if result["verdict"] == "FAIL")
    inconclusive_count = sum(1 for result in results if result["verdict"] == "INCONCLUSIVE")

    failures_by_category: dict[str, int] = {}
    artifact_pointers: list[str] = []
    blocking_failure = False
    yellow_signal = inconclusive_count > 0

    for result in results:
        if result["verdict"] != "PASS":
            failures_by_category[result["batch"]] = failures_by_category.get(result["batch"], 0) + 1
            artifact_pointers.append(result["artifacts"]["result_file"])
        if result["verdict"] == "FAIL" and result.get("gate") == "must-pass":
            blocking_failure = True
        if result["verdict"] != "PASS":
            yellow_signal = True

    release_gate = "RED" if blocking_failure else "YELLOW" if yellow_signal else "GREEN"
    summary = {
        "total_scenarios": total,
        "pass": pass_count,
        "fail": fail_count,
        "inconclusive": inconclusive_count,
        "failures_by_category": failures_by_category,
        "artifact_pointers": artifact_pointers,
        "release_gate": release_gate,
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print(json.dumps(summary, indent=2))
    return 0 if release_gate != "RED" else 1


def ensure_wiki_dirs(wiki_root: Path) -> None:
    for rel_path in ("raw/ingest", "candidate/reports", "candidate/patches", "canonical", "system"):
        (wiki_root / rel_path).mkdir(parents=True, exist_ok=True)


def copy_tree_contents(source_root: Path, destination_root: Path) -> None:
    if not source_root.exists():
        return
    for path in sorted(source_root.rglob("*")):
        rel_path = path.relative_to(source_root)
        target = destination_root / rel_path
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def apply_setup_steps(steps: list[dict[str, Any]], context: dict[str, str]) -> None:
    for step in steps:
        action = step["action"]
        if action == "copy_file":
            source = (FIXTURE_ROOT / resolve_value(step["from"], context)).resolve()
            target = resolve_scoped_path(step["to_scope"], resolve_value(step["to"], context), context)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        elif action == "copy_tree":
            source = (FIXTURE_ROOT / resolve_value(step["from"], context)).resolve()
            target = resolve_scoped_path(step["to_scope"], resolve_value(step["to"], context), context)
            target.mkdir(parents=True, exist_ok=True)
            copy_tree_contents(source, target)
        elif action == "write_file":
            target = resolve_scoped_path(step["scope"], resolve_value(step["path"], context), context)
            target.parent.mkdir(parents=True, exist_ok=True)
            if "from" in step:
                text = (FIXTURE_ROOT / resolve_value(step["from"], context)).read_text(encoding="utf-8")
            else:
                text = resolve_value(step["content"], context)
            target.write_text(text, encoding="utf-8")
        elif action == "replace_text":
            target = resolve_scoped_path(step["scope"], resolve_value(step["path"], context), context)
            text = target.read_text(encoding="utf-8")
            new_text = text.replace(resolve_value(step["old"], context), resolve_value(step["new"], context), step.get("count", -1))
            if new_text == text:
                die(f"replace_text did not modify {target}")
            target.write_text(new_text, encoding="utf-8")
        elif action == "remove_regex":
            target = resolve_scoped_path(step["scope"], resolve_value(step["path"], context), context)
            text = target.read_text(encoding="utf-8")
            new_text, count = re.subn(resolve_value(step["pattern"], context), "", text, flags=re.MULTILINE | re.DOTALL)
            if count == 0:
                die(f"remove_regex did not modify {target}")
            target.write_text(new_text, encoding="utf-8")
        else:
            die(f"unknown setup action: {action}")


def extract_captures(captures: list[dict[str, Any]], stdout_text: str, stderr_text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for capture in captures:
        source_text = stdout_text if capture["source"] == "stdout" else stderr_text
        match = re.search(capture["pattern"], source_text, flags=re.MULTILINE)
        if not match:
            values[capture["name"]] = ""
            continue
        values[capture["name"]] = match.group("value")
    return values


def record_exit_assertion(expected_exit: str, exit_code: int, assertions: list[dict[str, Any]]) -> None:
    if expected_exit == "success":
        assertions.append(assertion("exit_code", exit_code == 0, f"expected 0, got {exit_code}"))
    elif expected_exit == "blocked":
        assertions.append(assertion("exit_code", exit_code != 0, f"expected nonzero, got {exit_code}"))
    elif expected_exit == "warning":
        assertions.append(assertion("exit_code", exit_code == 0, f"expected 0 with warnings, got {exit_code}"))
    else:
        assertions.append(assertion("exit_code", False, f"unknown expected_exit: {expected_exit}"))


def evaluate_output_expectations(
    stream_name: str, expectations: list[Any], text: str, context: dict[str, str], assertions: list[dict[str, Any]]
) -> None:
    for index, expectation in enumerate(expectations, start=1):
        mode, expected = normalize_expectation(expectation, context)
        label = f"{stream_name}_{mode}_{index}"
        if mode == "contains":
            assertions.append(assertion(label, expected in text, summarize_match(text, expected)))
        elif mode == "not_contains":
            assertions.append(assertion(label, expected not in text, summarize_negative_match(text, expected)))
        elif mode == "regex":
            matched = re.search(expected, text, flags=re.MULTILINE) is not None
            assertions.append(assertion(label, matched, f"regex={expected}"))
        elif mode == "not_regex":
            matched = re.search(expected, text, flags=re.MULTILINE) is None
            assertions.append(assertion(label, matched, f"regex={expected}"))
        else:
            assertions.append(assertion(label, False, f"unknown expectation mode: {mode}"))


def evaluate_warning_expectations(
    expectations: list[Any], text: str, context: dict[str, str], assertions: list[dict[str, Any]]
) -> None:
    for index, expectation in enumerate(expectations, start=1):
        mode, expected = normalize_expectation(expectation, context)
        label = f"warning_{mode}_{index}"
        if mode == "contains":
            assertions.append(assertion(label, expected in text, summarize_match(text, expected)))
        elif mode == "regex":
            matched = re.search(expected, text, flags=re.MULTILINE) is not None
            assertions.append(assertion(label, matched, f"regex={expected}"))
        else:
            assertions.append(assertion(label, False, f"unsupported warning expectation mode: {mode}"))


def evaluate_file_expectations(expectations: list[dict[str, Any]], context: dict[str, str], assertions: list[dict[str, Any]]) -> None:
    for index, expectation in enumerate(expectations, start=1):
        expectation = resolve_value(expectation, context)
        assertion_type = expectation.get("assertion", "exists")
        label = f"file_{assertion_type}_{index}"
        if assertion_type == "glob_count":
            base = resolve_scope_root(expectation["scope"], context)
            matches = sorted(base.glob(expectation["glob"]))
            assertions.append(
                assertion(
                    label,
                    len(matches) == expectation["count"],
                    f"glob={expectation['glob']} count={len(matches)} expected={expectation['count']}",
                )
            )
            continue

        path = resolve_scoped_path(expectation["scope"], expectation["path"], context)
        exists = path.exists()
        type_ok = True
        if expectation.get("type") == "file":
            type_ok = path.is_file()
        elif expectation.get("type") == "dir":
            type_ok = path.is_dir()
        checks = [exists, type_ok]
        details = [f"path={path}", f"exists={exists}", f"type_ok={type_ok}"]
        if exists and path.is_file():
            text = path.read_text(encoding="utf-8")
            for contains in expectation.get("contains", []):
                ok = contains in text
                checks.append(ok)
                details.append(f"contains={contains!r}:{ok}")
            for not_contains in expectation.get("not_contains", []):
                ok = not_contains not in text
                checks.append(ok)
                details.append(f"not_contains={not_contains!r}:{ok}")
            fixture_path = expectation.get("equals_fixture")
            if fixture_path:
                expected_text = (FIXTURE_ROOT / fixture_path).read_text(encoding="utf-8")
                ok = text == expected_text
                checks.append(ok)
                details.append(f"equals_fixture={fixture_path}:{ok}")
        assertions.append(assertion(label, all(checks), "; ".join(details)))


def evaluate_forbidden_paths(entries: list[dict[str, Any]], context: dict[str, str], assertions: list[dict[str, Any]]) -> None:
    for index, entry in enumerate(entries, start=1):
        entry = resolve_value(entry, context)
        path = resolve_scoped_path(entry["scope"], entry["path"], context)
        assertions.append(assertion(f"forbidden_path_{index}", not path.exists(), f"path={path} exists={path.exists()}"))


def evaluate_watch_paths(watch_paths: list[str], baseline_hashes: dict[str, Any], assertions: list[dict[str, Any]]) -> None:
    for index, rel_path in enumerate(watch_paths, start=1):
        current_hash = hash_optional(REPO_ROOT / rel_path)
        assertions.append(
            assertion(
                f"repo_unchanged_{index}",
                current_hash == baseline_hashes.get(rel_path),
                f"path={rel_path} baseline={baseline_hashes.get(rel_path)} current={current_hash}",
            )
        )


def normalize_expectation(expectation: Any, context: dict[str, str]) -> tuple[str, str]:
    if isinstance(expectation, str):
        return "contains", resolve_value(expectation, context)
    return expectation["mode"], resolve_value(expectation.get("text") or expectation.get("pattern"), context)


def resolve_scope_root(scope: str, context: dict[str, str]) -> Path:
    if scope == "wiki_root":
        return Path(context["wiki_root"])
    if scope == "workspace_root":
        return Path(context["workspace_root"])
    if scope == "fixture_root":
        return Path(context["fixture_root"])
    if scope == "repo_root":
        return Path(context["repo_root"])
    if scope == "absolute":
        return Path("/")
    die(f"unknown scope: {scope}")
    return Path("/")


def resolve_scoped_path(scope: str, path: str, context: dict[str, str]) -> Path:
    resolved_path = resolve_value(path, context)
    if scope == "absolute":
        return Path(resolved_path).expanduser().resolve()
    return (resolve_scope_root(scope, context) / resolved_path).resolve()


def resolve_value(value: Any, context: dict[str, str]) -> Any:
    if isinstance(value, str):
        return value.format_map(SafeDict(context))
    if isinstance(value, list):
        return [resolve_value(item, context) for item in value]
    if isinstance(value, dict):
        return {key: resolve_value(item, context) for key, item in value.items()}
    return value


def extract_lines(text: str, prefix: str) -> list[str]:
    pattern = re.compile(rf"^{prefix}: .*?$", flags=re.MULTILINE)
    return pattern.findall(text)


def hash_optional(path: Path) -> str | None:
    if not path.exists():
        return None
    if path.is_dir():
        digest = hashlib.sha256()
        for child in sorted(path.rglob("*")):
            digest.update(str(child.relative_to(path)).encode())
            if child.is_file():
                digest.update(hashlib.sha256(child.read_bytes()).digest())
        return digest.hexdigest()
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assertion(name: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"name": name, "pass": passed, "evidence": evidence}


def summarize_match(text: str, needle: str) -> str:
    return f"found={needle!r}" if needle in text else f"missing={needle!r}"


def summarize_negative_match(text: str, needle: str) -> str:
    return f"absent={needle!r}" if needle not in text else f"unexpectedly_present={needle!r}"


class SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def die(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(2)


if __name__ == "__main__":
    raise SystemExit(main())
