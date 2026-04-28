#!/usr/bin/env python3
import sys, os, glob, json, shutil, subprocess
import numpy as np

DATA_DIR = "/Users/stan/code/toolkit/brain/data"
ENV_FILE = "/Users/stan/code/toolkit/brain/.env"
WORKSPACE = "/Users/stan/code/toolkit/brain"
SPEAKERS_FILE = os.path.join(DATA_DIR, "speakers.json")
VOCAB_FILE = os.path.join(DATA_DIR, "vocab.txt")
SIMILARITY_THRESHOLD = 0.75
POLISH_MODEL = "claude-4.7-opus-max-thinking"
POLISH_TIMEOUT = 1800
PROJECT_CONTEXT_FILES = [
    os.path.expanduser("~/code/pronet/CLAUDE.local.md"),
    os.path.expanduser("~/code/sky/CLAUDE.local.md"),
]

def load_hf_token():
    if os.path.exists(ENV_FILE):
        for line in open(ENV_FILE):
            if line.startswith("HF_TOKEN="):
                return line.strip().split("=", 1)[1]
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("Error: HF_TOKEN not found. Create .env with HF_TOKEN=hf_xxx", file=sys.stderr)
        sys.exit(1)
    return token

def find_latest_wav():
    files = sorted(glob.glob(os.path.join(DATA_DIR, "rec-*.wav")), reverse=True)
    if not files:
        print(f"No rec-*.wav files found in {DATA_DIR}", file=sys.stderr)
        sys.exit(1)
    return files[0]

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    dot = np.dot(a, b)
    norm = np.linalg.norm(a) * np.linalg.norm(b)
    return dot / norm if norm > 0 else 0.0

def load_known_speakers():
    if not os.path.exists(SPEAKERS_FILE):
        return {}
    with open(SPEAKERS_FILE) as f:
        return json.load(f)

def match_speakers(new_embeddings, known_speakers):
    """Match new speaker embeddings against known profiles. Returns {SPEAKER_XX: "Name"} map."""
    rename_map = {}
    if not known_speakers or not new_embeddings:
        return rename_map

    used_names = set()
    scored = []
    for spk_id, emb in new_embeddings.items():
        for name, profile in known_speakers.items():
            sim = cosine_similarity(emb, profile["embedding"])
            scored.append((sim, spk_id, name))

    for sim, spk_id, name in sorted(scored, reverse=True):
        if sim < SIMILARITY_THRESHOLD:
            break
        if spk_id in rename_map or name in used_names:
            continue
        rename_map[spk_id] = name
        used_names.add(name)
        print(f"  Matched {spk_id} -> {name} (similarity: {sim:.3f})")

    return rename_map

def build_initial_prompt(wav_basename):
    """Build Whisper initial_prompt from filename and vocab file for vocabulary priming."""
    parts = wav_basename.replace("rec-", "").replace(".wav", "").split("-", 4)
    names = parts[4].replace("-", " ").split("  ") if len(parts) > 4 else []
    meeting_name = parts[4].replace("-", " ") if len(parts) > 4 else ""

    prompt_parts = []
    if names:
        prompt_parts.append(f"Participants: {', '.join(names)}.")
    if meeting_name:
        prompt_parts.append(f"Meeting: {meeting_name}.")

    if os.path.exists(VOCAB_FILE):
        vocab = open(VOCAB_FILE).read().strip()
        if vocab:
            prompt_parts.append(f"Terms: {vocab}")

    return " ".join(prompt_parts) if prompt_parts else None


def load_project_context():
    """Load project context files for summary generation."""
    sections = []
    for path in PROJECT_CONTEXT_FILES:
        if os.path.exists(path):
            name = os.path.basename(os.path.dirname(path))
            content = open(path).read().strip()
            if content:
                sections.append(f"### Project: {name}\n{content}")
    return "\n\n".join(sections)


def polish_and_summarize(txt_file):
    """Correct transcript and generate summary + to-dos in a single agent call."""
    agent_path = shutil.which("agent")
    if not agent_path:
        print("  Agent CLI not found, skipping polish + summary")
        return

    rel_txt = os.path.relpath(txt_file, WORKSPACE)
    polished_out = os.path.relpath(txt_file.replace(".txt", ".polished.txt"), WORKSPACE)
    summary_out = os.path.relpath(txt_file.replace(".txt", ".summary.md"), WORKSPACE)

    project_context = load_project_context()
    context_block = ""
    if project_context:
        context_block = (
            f"\nUse the following project context to make better inferences "
            f"about what the discussed topics relate to and what to-dos are relevant:\n\n"
            f"{project_context}\n"
        )

    prompt = (
        f"Read the file {rel_txt}. This is a raw Whisper transcription of a meeting.\n"
        f"You have TWO tasks.\n\n"
        f"━━━ TASK 1: Correct the transcript ━━━\n\n"
        f"Output a corrected version of the ENTIRE transcript. Fix ONLY obvious transcription errors:\n"
        f"- Words that are clearly misheard (wrong homophones, nonsense words, garbled domain terms)\n"
        f"- Repeated gibberish fragments\n"
        f"- Clearly wrong punctuation that changes meaning\n\n"
        f"For single-word corrections where context strongly indicates the right word\n"
        f"(abbreviations: AA→AI, homophones: takes→tags, near-misses: depth→debt),\n"
        f"go ahead and make the fix. These are low-risk, high-clarity improvements.\n"
        f"Only hesitate on corrections that could change the speaker's intended meaning.\n\n"
        # f"For expressions that appear to be non-native idioms, culturally-specific phrases,\n"
        # f"or unclear but possibly intentional wording, keep the original text but add a\n"
        # f"brief bracketed note for the reader's context. For example:\n"
        # f'  "killing my heavens [Turkish idiom for \'beating myself up\']"\n'
        # f'  "million knows [misheard name]"\n'
        # f"Keep notes concise -- a few words, not a sentence.\n\n"
        f"For passages that remain unintelligible even after considering context,\n"
        f"add an [unclear] or [inaudible] marker so readers know the text is unreliable.\n\n"
        f"Do NOT:\n"
        f"- Rephrase or improve anyone's speech\n"
        f"- Fix grammar (non-native speakers' grammar IS their speech)\n"
        f"- Remove filler words (um, uh, like)\n"
        f"- Add commentary or explanations\n\n"
        f"- Never translate Spanish to English\n\n"
        # f"- Add commentary or explanations outside of the bracketed notes described above\n\n"
        f"Keep timestamps and the original structure exactly as-is.\n"
        f"NEVER change speaker labels. Speaker names were assigned by voice matching and must not be altered.\n"
        f"The filename may contain a calendar event name — this does NOT reliably indicate who is in the call.\n"
        f"Participants may have joined after the calendar event ended, or the call may be unrelated to the event.\n"
        f"For long speaker turns, insert paragraph breaks at natural topic shifts to improve readability.\n"
        f"Keep the speaker label and timestamp on the first paragraph only.\n"
        f"Write the corrected transcript to {polished_out}\n\n"
        f"━━━ TASK 2: Generate a summary ━━━\n\n"
        f"After correcting the transcript, generate a structured summary for Stan (always a participant).\n\n"
        f"If the conversation content does not match the calendar event name in the filename,\n"
        f"add a first line: ## Title: <descriptive name for the actual conversation>\n"
        f"Only add this line when the filename is misleading. Otherwise omit it.\n\n"
        f"## Summary\n"
        f"A concise 3-7 bullet point summary covering: key topics discussed, decisions made, and open questions.\n\n"
        f"## To-Dos\n"
        f"Extract actionable to-dos. For each:\n"
        f"- Include the timestamp [MM:SS] where it was discussed\n"
        f"- Brief description of the task\n"
        f"- Who is responsible (bold the name)\n\n"
        f"Default assumption: if a task was discussed but not explicitly assigned to someone else, "
        f"it is Stan's task. Stan works on Sierra agent projects and is responsible for technical "
        f"implementation and client-facing coordination.\n\n"
        f"Format each to-do as: - [ ] [MM:SS] Description — **Name**\n"
        f"{context_block}\n"
        f"Write the summary to {summary_out}"
    )

    reasoning_file = txt_file.replace(".txt", ".reasoning.jsonl")

    print("  Correcting + summarizing with LLM...")
    try:
        result = subprocess.run(
            [agent_path, "--print", "--output-format", "stream-json",
             "--stream-partial-output", "--trust", "--force",
             "--model", POLISH_MODEL, "--workspace", WORKSPACE, prompt],
            capture_output=True, text=True, timeout=POLISH_TIMEOUT,
        )
        if result.stdout.strip():
            with open(reasoning_file, "w") as f:
                f.write(result.stdout)
            print(f"  Reasoning saved ({os.path.getsize(reasoning_file)} bytes)")

        polished_file = txt_file.replace(".txt", ".polished.txt")
        summary_file = txt_file.replace(".txt", ".summary.md")
        if os.path.exists(polished_file):
            print(f"  Polished transcript saved ({os.path.getsize(polished_file)} bytes)")
        else:
            print(f"  Polish: output file not created")
        if os.path.exists(summary_file):
            print(f"  Summary saved ({os.path.getsize(summary_file)} bytes)")
        else:
            print(f"  Summary: output file not created")
    except subprocess.TimeoutExpired:
        print(f"  Timed out after {POLISH_TIMEOUT}s")
    except Exception as e:
        print(f"  Error — {e}")


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg:
        wav_file = arg if arg.startswith("/") else os.path.join(DATA_DIR, arg)
    else:
        wav_file = find_latest_wav()

    if not os.path.exists(wav_file):
        print(f"File not found: {wav_file}", file=sys.stderr)
        sys.exit(1)

    hf_token = load_hf_token()
    base = wav_file.rsplit(".wav", 1)[0]
    basename = os.path.basename(wav_file)
    print(f"Transcribing {basename}...")

    initial_prompt = build_initial_prompt(basename)
    if initial_prompt:
        print(f"  Vocabulary hint: {initial_prompt[:100]}...")

    import whispermlx

    print("  Loading model...")
    asr_options = {"initial_prompt": initial_prompt} if initial_prompt else None
    model = whispermlx.load_model("large-v3", device="cpu", asr_options=asr_options)

    print("  Transcribing...")
    result = model.transcribe(wav_file)
    language = result.get("language", "unknown")
    print(f"  Language: {language}")

    print("  Aligning words...")
    model_a, metadata = whispermlx.load_align_model(language_code=language, device="cpu")
    result = whispermlx.align(result["segments"], model_a, metadata, wav_file, device="cpu")

    print("  Diarizing speakers...")
    from whispermlx.diarize import DiarizationPipeline

    diarize_model = DiarizationPipeline(token=hf_token, device="mps")
    diarize_df, speaker_embeddings = diarize_model(
        wav_file, min_speakers=2, max_speakers=8, return_embeddings=True
    )
    n_speakers = diarize_df["speaker"].nunique() if len(diarize_df) > 0 else 0
    print(f"  Detected {n_speakers} speakers in {len(diarize_df)} segments")

    result = whispermlx.assign_word_speakers(
        diarize_df, result, speaker_embeddings=speaker_embeddings, fill_nearest=True
    )

    known_speakers = load_known_speakers()
    rename_map = match_speakers(speaker_embeddings or {}, known_speakers)

    def label(spk):
        return rename_map.get(spk, spk)

    speakers = set()
    turns = []
    current_speaker = None
    current_ts = None
    current_texts = []

    for seg in result["segments"]:
        speaker = label(seg.get("speaker", "UNKNOWN"))
        speakers.add(speaker)
        text = seg.get("text", "").strip()
        if not text:
            continue
        if speaker != current_speaker:
            if current_speaker is not None:
                turns.append((current_ts, current_speaker, " ".join(current_texts)))
            start = seg.get("start", 0)
            h, m, s = int(start // 3600), int((start % 3600) // 60), int(start % 60)
            current_ts = f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
            current_speaker = speaker
            current_texts = [text]
        else:
            current_texts.append(text)

    if current_speaker is not None:
        turns.append((current_ts, current_speaker, " ".join(current_texts)))

    lines = [f"Language: {language}", f"Speakers: {len(speakers)}", ""]
    for ts, speaker, text in turns:
        lines.append(f"[{ts}] {speaker}: {text}")
        lines.append("")

    txt_file = base + ".txt"
    with open(txt_file, "w") as f:
        f.write("\n".join(lines) + "\n")

    json_file = base + ".json"
    with open(json_file, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\nTranscript saved to {os.path.basename(txt_file)} ({len(speakers)} speakers)")

    polish_and_summarize(txt_file)

if __name__ == "__main__":
    main()
