#!/usr/bin/env python3
"""Polish all raw transcripts, then run 2 review agents per polished output."""

import subprocess, os, sys, time, json, glob
from concurrent.futures import ThreadPoolExecutor, as_completed

WORKSPACE = "/Users/stan/code/rec"
DATA_DIR = os.path.join(WORKSPACE, "data")
AGENT = "/Users/stan/.local/bin/agent"
POLISH_MODEL = "claude-4.6-opus-max-thinking"
SUMMARY_MODEL = "claude-4.6-opus-max-thinking"
REVIEW_MODEL = "claude-4.5-opus-high-thinking"
POLISH_TIMEOUT = 1800
SUMMARY_TIMEOUT = 600
REVIEW_TIMEOUT = 600

PROJECT_CONTEXT_FILES = [
    os.path.expanduser("~/code/pronet/CLAUDE.local.md"),
    os.path.expanduser("~/code/sky/CLAUDE.local.md"),
]


def get_transcripts():
    txts = sorted(glob.glob(os.path.join(DATA_DIR, "rec-*.txt")))
    return [t for t in txts if not t.endswith(".polished.txt") and "-corrected" not in t]


def build_polish_prompt(txt_path):
    rel_txt = os.path.relpath(txt_path, WORKSPACE)
    rel_out = rel_txt.replace(".txt", ".polished.txt")
    return (
        f"Read the file {rel_txt}. "
        f"This is a raw Whisper transcription of a meeting.\n\n"
        f"Output a corrected version of the ENTIRE transcript. Fix ONLY obvious transcription errors:\n"
        f"- Words that are clearly misheard (wrong homophones, nonsense words, garbled domain terms)\n"
        f"- Repeated gibberish fragments\n"
        f"- Clearly wrong punctuation that changes meaning\n\n"
        f"For single-word corrections where context strongly indicates the right word\n"
        f"(abbreviations: AA→AI, homophones: takes→tags, near-misses: depth→debt),\n"
        f"go ahead and make the fix. These are low-risk, high-clarity improvements.\n"
        f"Only hesitate on corrections that could change the speaker's intended meaning.\n\n"
        f"For expressions that appear to be non-native idioms, culturally-specific phrases,\n"
        f"or unclear but possibly intentional wording, keep the original text but add a\n"
        f"brief bracketed note for the reader's context. For example:\n"
        f'  "killing my heavens [Turkish idiom for \'beating myself up\']"\n'
        f'  "million knows [misheard name]"\n'
        f"Keep notes concise -- a few words, not a sentence.\n\n"
        f"For passages that remain unintelligible even after considering context,\n"
        f"add an [unclear] or [inaudible] marker so readers know the text is unreliable.\n\n"
        f"Do NOT:\n"
        f"- Rephrase or improve anyone's speech\n"
        f"- Fix grammar (non-native speakers' grammar IS their speech)\n"
        f"- Remove filler words (um, uh, like)\n"
        f"- Add commentary or explanations outside of the bracketed notes described above\n\n"
        f"Keep timestamps and the original structure exactly as-is.\n"
        f"For speaker labels, fix obvious misattributions where the content clearly belongs to a different speaker.\n"
        f"For long speaker turns, insert paragraph breaks at natural topic shifts to improve readability.\n"
        f"Keep the speaker label and timestamp on the first paragraph only.\n"
        f"Output ONLY the corrected transcript, nothing else.\n"
        f"Write the result to {rel_out}"
    )


def load_project_context():
    sections = []
    for path in PROJECT_CONTEXT_FILES:
        if os.path.exists(path):
            name = os.path.basename(os.path.dirname(path))
            content = open(path).read().strip()
            if content:
                sections.append(f"### Project: {name}\n{content}")
    return "\n\n".join(sections)


def build_summary_prompt(txt_path):
    polished = txt_path.replace(".txt", ".polished.txt")
    source = polished if os.path.exists(polished) else txt_path
    rel_source = os.path.relpath(source, WORKSPACE)
    rel_out = os.path.relpath(txt_path.replace(".txt", ".summary.md"), WORKSPACE)

    project_context = load_project_context()
    context_block = ""
    if project_context:
        context_block = (
            f"\n\nUse the following project context to make better inferences "
            f"about what needs to happen and what the discussed topics relate to:\n\n"
            f"{project_context}\n"
        )

    return (
        f"Read the file {rel_source}. "
        f"This is a transcript of a meeting. You are summarizing it for Stan, who is always a participant.\n\n"
        f"Generate a structured summary with two sections:\n\n"
        f"## Summary\n"
        f"A concise 3-7 bullet point summary covering: key topics discussed, decisions made, and open questions.\n\n"
        f"## To-Dos\n"
        f"Extract actionable to-dos from the conversation. For each:\n"
        f"- Include the timestamp [MM:SS] where it was discussed\n"
        f"- Brief description of the task\n"
        f"- Who is responsible (bold the name)\n\n"
        f"Default assumption: if a task was discussed but not explicitly assigned to someone else, "
        f"it is Stan's task. Stan works on Sierra agent projects and is responsible for technical "
        f"implementation and client-facing coordination.\n\n"
        f"Format each to-do as: - [ ] [MM:SS] Description — **Name**\n"
        f"{context_block}\n"
        f"Output ONLY the markdown summary, nothing else.\n"
        f"Write the result to {rel_out}"
    )


def build_review_prompt(raw_path, polished_path, reviewer_id):
    rel_raw = os.path.relpath(raw_path, WORKSPACE)
    rel_pol = os.path.relpath(polished_path, WORKSPACE)
    return (
        f"You are Reviewer {reviewer_id}. Your job is to evaluate the quality of a transcript correction.\n\n"
        f"Read both files:\n"
        f"- Raw transcript: {rel_raw}\n"
        f"- Polished transcript: {rel_pol}\n\n"
        f"Compare them and produce a structured review:\n\n"
        f"1. **Changes made**: List every difference between raw and polished. For each, state whether it is:\n"
        f"   - CORRECT: Clearly fixes a transcription error\n"
        f"   - HARMFUL: Changes meaning, removes valid content, or overwrites the speaker's actual phrasing\n"
        f"   - NEUTRAL: Neither helpful nor harmful (formatting, stylistic)\n\n"
        f"2. **Missed errors**: List obvious transcription errors in the raw that were NOT fixed in the polished version.\n\n"
        f"3. **Bracketed notes**: Evaluate any [bracketed notes] added. Are they accurate? Helpful? Excessive?\n\n"
        f"4. **Overall score** (1-10): Rate the quality of the correction, where:\n"
        f"   - 10 = Every real error fixed, zero harmful changes, perfect notes\n"
        f"   - 7 = Most errors fixed, no harmful changes\n"
        f"   - 5 = Some errors fixed but significant misses or a few harmful changes\n"
        f"   - 3 = Many errors missed or several harmful changes\n\n"
        f"Be specific and cite timestamps when referencing changes.\n"
        f"Output your review as markdown."
    )


def run_agent(model, prompt, timeout, label, reasoning_path=None):
    use_stream = reasoning_path is not None
    fmt_args = (["--output-format", "stream-json", "--stream-partial-output"]
                if use_stream else ["--output-format", "text"])
    start = time.time()
    try:
        result = subprocess.run(
            [AGENT, "--print"] + fmt_args + ["--trust", "--force",
             "--model", model, "--workspace", WORKSPACE, prompt],
            capture_output=True, text=True, timeout=timeout,
        )
        elapsed = time.time() - start
        if result.returncode != 0:
            print(f"  [{label}] FAILED ({elapsed:.0f}s)")
            return None

        if use_stream and result.stdout.strip():
            with open(reasoning_path, "w") as f:
                f.write(result.stdout)

        print(f"  [{label}] OK ({elapsed:.0f}s)")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"  [{label}] TIMEOUT ({time.time()-start:.0f}s)")
        return None


def main():
    transcripts = get_transcripts()
    print(f"Found {len(transcripts)} transcripts to polish\n")

    # Phase 1: Polish all transcripts
    print("=" * 60)
    print("PHASE 1: Polishing transcripts with Opus")
    print("=" * 60)

    to_polish = []
    for txt in transcripts:
        polished = txt.replace(".txt", ".polished.txt")
        if os.path.exists(polished) and os.path.getsize(polished) > 5000:
            print(f"  SKIP (exists): {os.path.basename(txt)}")
        else:
            to_polish.append(txt)

    if to_polish:
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {}
            for txt in to_polish:
                prompt = build_polish_prompt(txt)
                label = os.path.basename(txt)[:40]
                reasoning = txt.replace(".txt", ".reasoning.jsonl")
                futures[pool.submit(run_agent, POLISH_MODEL, prompt, POLISH_TIMEOUT,
                                    f"polish:{label}", reasoning_path=reasoning)] = txt
            for f in as_completed(futures):
                f.result()
    print()

    # Phase 1.5: Summarize all transcripts
    print("=" * 60)
    print("PHASE 1.5: Generating summaries with Opus")
    print("=" * 60)

    to_summarize = []
    for txt in transcripts:
        summary = txt.replace(".txt", ".summary.md")
        if os.path.exists(summary) and os.path.getsize(summary) > 100:
            print(f"  SKIP (exists): {os.path.basename(txt)}")
        else:
            to_summarize.append(txt)

    if to_summarize:
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures = {}
            for txt in to_summarize:
                prompt = build_summary_prompt(txt)
                label = os.path.basename(txt)[:40]
                reasoning = txt.replace(".txt", ".summary-reasoning.jsonl")
                futures[pool.submit(run_agent, SUMMARY_MODEL, prompt, SUMMARY_TIMEOUT,
                                    f"summary:{label}", reasoning_path=reasoning)] = txt
            for f in as_completed(futures):
                f.result()
    print()

    # Phase 2: Review each polished transcript with 2 reviewers
    print("=" * 60)
    print("PHASE 2: Reviewing polished transcripts (2 reviewers each)")
    print("=" * 60)

    reviews_dir = os.path.join(DATA_DIR, "reviews")
    os.makedirs(reviews_dir, exist_ok=True)

    review_futures = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for txt in transcripts:
            polished = txt.replace(".txt", ".polished.txt")
            if not os.path.exists(polished) or os.path.getsize(polished) < 100:
                print(f"  SKIP (no polished): {os.path.basename(txt)}")
                continue

            base = os.path.basename(txt).replace(".txt", "")
            for rid in [1, 2]:
                review_path = os.path.join(reviews_dir, f"{base}.review-{rid}.md")
                if os.path.exists(review_path) and os.path.getsize(review_path) > 100:
                    print(f"  SKIP (exists): {base} reviewer {rid}")
                    continue

                prompt = build_review_prompt(txt, polished, rid)
                label = f"review:{base[:30]}:R{rid}"
                fut = pool.submit(run_agent, REVIEW_MODEL, prompt, REVIEW_TIMEOUT, label)
                review_futures[fut] = review_path

        for fut in as_completed(review_futures):
            path = review_futures[fut]
            output = fut.result()
            if output:
                with open(path, "w") as f:
                    f.write(output + "\n")

    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)
    print(f"\nPolished transcripts: {DATA_DIR}/rec-*.polished.txt")
    print(f"Reviews: {reviews_dir}/")


if __name__ == "__main__":
    main()
