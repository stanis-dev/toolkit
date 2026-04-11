#!/usr/bin/env python3
"""Run 3 models x 10 sessions on the same transcript polish prompt, saving outputs for evaluation."""

import subprocess, os, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

WORKSPACE = "/Users/stan/code/rec"
EVAL_DIR = os.path.join(WORKSPACE, "data/eval")
PROMPT_FILE = os.path.join(EVAL_DIR, "prompt.txt")
AGENT = "/Users/stan/.local/bin/agent"

MODELS = {
    "opus": "claude-4.6-opus-max-thinking",
    "gpt": "gpt-5.4-xhigh",
    "gemini": "gemini-3.1-pro",
}

RUNS_PER_MODEL = 10
MAX_CONCURRENT = 5


def run_agent(model_id: str, model_label: str, run_num: int, prompt: str) -> dict:
    out_path = os.path.join(EVAL_DIR, model_label, f"run-{run_num:02d}.txt")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
        print(f"  [{model_label}] run-{run_num:02d}: already exists, skipping")
        return {"model": model_label, "run": run_num, "status": "skipped", "seconds": 0}

    start = time.time()
    try:
        result = subprocess.run(
            [AGENT, "--print", "--output-format", "text", "--trust",
             "--model", model_id, "--workspace", WORKSPACE, prompt],
            capture_output=True, text=True, timeout=1800,
        )
        elapsed = time.time() - start
        if result.returncode != 0:
            print(f"  [{model_label}] run-{run_num:02d}: FAILED ({elapsed:.1f}s) — {result.stderr[:200]}")
            return {"model": model_label, "run": run_num, "status": "error", "seconds": elapsed}

        output = result.stdout.strip()
        with open(out_path, "w") as f:
            f.write(output + "\n")

        print(f"  [{model_label}] run-{run_num:02d}: OK ({elapsed:.1f}s, {len(output)} chars)")
        return {"model": model_label, "run": run_num, "status": "ok", "seconds": elapsed, "chars": len(output)}

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"  [{model_label}] run-{run_num:02d}: TIMEOUT ({elapsed:.1f}s)")
        return {"model": model_label, "run": run_num, "status": "timeout", "seconds": elapsed}


def main():
    with open(PROMPT_FILE) as f:
        prompt = f.read().strip()

    print(f"Prompt: {len(prompt)} chars")
    print(f"Models: {', '.join(f'{k}={v}' for k, v in MODELS.items())}")
    print(f"Runs per model: {RUNS_PER_MODEL}, max concurrent: {MAX_CONCURRENT}")
    print()

    all_results = []

    for label, model_id in MODELS.items():
        print(f"=== {label} ({model_id}) ===")
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as pool:
            futures = {
                pool.submit(run_agent, model_id, label, i, prompt): i
                for i in range(1, RUNS_PER_MODEL + 1)
            }
            for future in as_completed(futures):
                all_results.append(future.result())
        print()

    ok = [r for r in all_results if r["status"] == "ok"]
    skip = [r for r in all_results if r["status"] == "skipped"]
    fail = [r for r in all_results if r["status"] not in ("ok", "skipped")]
    print(f"Done: {len(ok)} succeeded, {len(skip)} skipped, {len(fail)} failed")

    if ok:
        for label in MODELS:
            model_ok = [r for r in ok if r["model"] == label]
            if model_ok:
                avg = sum(r["seconds"] for r in model_ok) / len(model_ok)
                print(f"  {label}: {len(model_ok)} runs, avg {avg:.1f}s")


if __name__ == "__main__":
    main()
