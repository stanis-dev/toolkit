#!/usr/bin/env python3
"""Print Studio content from .composer as a flat outline, one line per piece of text.

Usage:
  blocks.py                 outline of the .composer found by walking up from the working directory,
                            or of every agents/*/.composer when run from the repository root
  blocks.py <agent-dir>     outline of one agent directory

Each line is tab-separated: path, text, JSON pointer.
  path     Studio display names of the enclosing block and steps, then the ordinal position of
           unnamed levels joined with dots: `Reactivación › Por qué dejó de usarla › 1.3.1`.
           Non-text nodes get a suffix: `trigger`, `si` (condition predicates), `tool`, `tags`,
           `goal`, `component`, `disabled`, `supervised`.
  text     the full string, newlines shown as ⏎
  pointer  where the string sits in the JSON file: `.children[1].items[0].subList.items[2]`

Files start with a `# <path> <type> <uuid>` line, in the order the context renders. Blocks,
components and config records are covered; conflict markers in a file stop the run.
"""

import glob
import json
import os
import sys

META_KEYS = {"_source_reasoning", "_policy_reasoning", "_trigger_reasoning", "$uuid"}
SKIP_KEYS = {
    "type", "name", "title", "goal", "text", "trigger_condition", "condition", "collapsed", "id",
    "key", "isNumbered", "noCodeId", "disabled", "supervised", "tags", "component_id", "list_type",
}


def fail(message):
    sys.stderr.write(message + "\n")
    sys.exit(1)


def composer_dirs(argv):
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)
    if argv:
        target = argv[0]
        for c in (target, os.path.join(target, ".composer")):
            if os.path.isdir(c) and os.path.isdir(os.path.join(c, "blocks")):
                return [c]
        fail(f"{target} has no .composer/blocks")
    d = os.getcwd()
    while True:
        c = os.path.join(d, ".composer")
        if os.path.isdir(os.path.join(c, "blocks")):
            return [c]
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    found = sorted(glob.glob(os.path.join(os.getcwd(), "agents", "*", ".composer", "blocks")))
    if not found:
        fail("no .composer directory found from " + os.getcwd())
    return [os.path.dirname(f) for f in found]


def load(path):
    text = open(path, encoding="utf-8").read()
    if "<<<<<<< " in text or "\n>>>>>>> " in text:
        fail(f"{path}: git conflict markers, resolve them before reading")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        fail(f"{path}: {e}")


def predicate(p):
    kind = p.get("type")
    if kind == "observation":
        return p["text"]
    if kind == "group":
        return "(" + condition(p) + ")"
    if "key" in p:
        value = p.get("value", p.get("values", ""))
        return f"{kind}:{p['key']} {p.get('operator', '')} {value}".rstrip()
    return json.dumps(p, ensure_ascii=False)


def condition(cond):
    joiner = " O " if cond.get("conjunction") == "any" else " Y "
    return joiner.join(predicate(p) for p in cond.get("predicates", []))


def walk(node, names, ords, ptr):
    if isinstance(node, str):
        yield names, ords, ptr, node
        return
    if isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, names, ords + [i + 1], f"{ptr}[{i}]")
        return
    if not isinstance(node, dict):
        return
    if set(node) - META_KEYS == {"value"}:
        yield from walk(node["value"], names, ords, f"{ptr}.value")
        return
    label = node.get("name") or node.get("title")
    if label and (not names or names[-1] != label):
        names, ords = names + [label], []
    for flag in ("disabled", "supervised"):
        if node.get(flag):
            yield names, ords + [flag], f"{ptr}.{flag}", "true"
    if node.get("tags"):
        yield names, ords + ["tags"], f"{ptr}.tags", ", ".join(map(str, node["tags"]))
    if node.get("component_id"):
        yield names, ords + ["component"], f"{ptr}.component_id", str(node["component_id"])
    if "trigger_condition" in node:
        yield names, ords + ["trigger"], f"{ptr}.trigger_condition", condition(node["trigger_condition"])
    if isinstance(node.get("condition"), dict):
        yield names, ords + ["si"], f"{ptr}.condition", condition(node["condition"])
    if node.get("type") == "tool_ref":
        yield names, ords + ["tool"], ptr, node.get("noCodeId") or node.get("name", "")
    if isinstance(node.get("goal"), str):
        yield names, ords + ["goal"], f"{ptr}.goal", node["goal"]
    if "item" in node:
        yield names, ords, f"{ptr}.item", node["item"]
        yield from walk(node.get("subList", {}).get("items", []), names, ords, f"{ptr}.subList.items")
        return
    if isinstance(node.get("text"), str):
        yield names, ords, f"{ptr}.text", node["text"]
    containers = [k for k in ("items", "children", "steps") if k in node]
    for k in containers:
        yield from walk(node[k], names, ords, f"{ptr}.{k}")
    if containers:
        return
    for k, v in node.items():
        if k.startswith(("_", "$")) or k in SKIP_KEYS:
            continue
        if isinstance(v, (dict, list)):
            yield from walk(v, names + [k], [], f"{ptr}.{k}")
        elif isinstance(v, str) and len(v) > 24:
            yield names + [k], [], f"{ptr}.{k}", v


def line(names, ords, ptr, text):
    path = " › ".join(names + ([".".join(map(str, ords))] if ords else []))
    return f"{path}\t{text.replace(chr(10), '⏎')}\t{ptr}"


def outline(composer):
    files = (
        sorted(glob.glob(os.path.join(composer, "blocks", "*.json")))
        + sorted(glob.glob(os.path.join(composer, "components", "*", "definition.json")))
        + sorted(glob.glob(os.path.join(composer, "config", "*", "*.json")))
    )
    for f in files:
        d = load(f)
        rel = os.path.relpath(f, composer)
        if rel.startswith("components" + os.sep):
            top = os.path.basename(os.path.dirname(f))
        else:
            top = d.get("name") or d.get("entry_name") or d.get("type")
        print(f"# {rel}  {d.get('type') or d.get('type_name', '')}  {d.get('$uuid') or d.get('id', '')}")
        for row in walk(d, [top] if top else [], [], ""):
            print(line(*row))


def main():
    dirs = composer_dirs(sys.argv[1:])
    for composer in dirs:
        if len(dirs) > 1:
            print(f"## {os.path.relpath(os.path.dirname(composer))}")
        outline(composer)


if __name__ == "__main__":
    main()
