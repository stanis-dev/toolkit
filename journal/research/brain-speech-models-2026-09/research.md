# Brain speech pipeline: model check, September 2026

## Summary

Audit of the five model slots in the Brain app (dictation ASR, meeting ASR, word alignment, diarization, transcript polish LLM) against everything released through 2026-09-04, using model cards, official repos, the Open ASR Leaderboard result files, vendor docs and local measurements on the M4 Max. Three slots stay as they are. Two slots have a verified better alternative: the word aligner (Qwen3-ForcedAligner-0.6B) and the diarizer (DiariZen). One config fix applies to the polish step.

Machine: Apple M4 Max, 64 GB, macOS 26.6.2. Recordings: 15 to 90 min, 2 to 8 speakers, mostly Spanish with English technical terms. Current timings for a 30 min meeting: about 60 s Whisper, about 15 s alignment, about 60 s diarization, about 6.5 min polish.

## Key findings

| Slot | Current | Verdict | Best alternative and evidence |
|---|---|---|---|
| Dictation ASR | Parakeet TDT 0.6B v3 via parakeet-mlx 0.5.2 | Keep | Fastest entry on the leaderboard Spanish track (RTFx 3786) and within 0.6 WER of the best local open model on FLEURS es. Qwen3-ASR-1.7B is more accurate (en 4.31 vs 4.86, FLEURS es 2.92 vs 3.25) and gave the only perfect transcript on a code-switched test clip, but takes 3.8 to 4.4 s for an 18.7 s clip against 0.20 to 0.72 s. |
| Meeting ASR | Whisper large-v3 via whispermlx 3.13.1 | Keep | No local open model beats it on Spanish while also giving word timestamps and language detection. Spanish avg 3.35; the three open models below it (Cohere Transcribe 2.81, Voxtral Small 24B 2.91, Canary-1B-v2 3.23) each lack timestamps, language detection, or both. Whisper's English is weak (5.78, AMI 13.63, worst AMI in the top 50). |
| Word alignment | wav2vec2 CTC (VOXPOPULI es, WAV2VEC2 en) via whispermlx | Switch after trial | Qwen3-ForcedAligner-0.6B (2026-01-29, Apache 2.0): Spanish word-boundary shift 36.8 ms vs 108.0 ms for the wav2vec2 aligner in use, one model for es and en, claims code-switched support, runs in mlx-audio. Numbers are the authors' against MFA pseudo-labels; no third-party benchmark yet. |
| Diarization | pyannote community-1 via pyannote.audio 4.0.7 on MPS | Switch after trial | DiariZen wavlm-large-s80-md-v2 (2025-12): same no-collar protocol, AMI-SDM 13.9 vs 19.9, DIHARD3 14.5 vs 20.2, VoxConverse 9.1 vs 11.2, AliMeeting 10.8 vs 20.3. Costs: CC BY-NC 4.0 weights, cuda or cpu only, torch 2.1.1 pin means a separate venv, Mac speed unpublished. |
| Speaker identification | cosine 0.75 on community-1 centroids (WeSpeaker ResNet34, 256-d) | Upgrade candidate | ReDimNet2 B6 (2026-07-01, MIT): VoxCeleb1-O EER 0.29 percent vs about 0.8 for ResNet34. Needs a second embedding pass over each speaker's segments and re-enrollment of speakers.json. Gain on compressed Teams audio unverified. Recent match margin was thin (0.804 vs 0.75). |
| Polish LLM | claude-opus-5-thinking-high via cursor-agent | Keep, fix effort | Fable 5.1 is "NO ZDR" in Cursor: Anthropic stores prompt and output 30 days for harm review regardless of Privacy Mode, at 2x price, with multilingual "on par with Fable 5" and no benchmark that maps to Spanish transcript correction. Opus 5 runs under Cursor's ZDR agreement. |

### Dictation

- Parakeet v3 leaderboard Spanish: FLEURS 3.25, Common Voice 3.53, MLS 4.36; English 4.86. Source: `hf-audio/multilingual_evals/multilingual_es.csv` (2026-08-28) and `english_short_latest.csv`.
- Local latency (18.7 s Spanish clip with English terms): Parakeet cold process 1.5 to 2.1 s total, of which 0.7 to 1.1 s is interpreter start plus model load and 0.55 to 0.72 s is the first transcription; warm transcription 0.20 s. A separate run on a 20 s clip: 3.09 s spawn to ready, 1.58 s first transcription. The app already hides the load behind the user's speech.
- Alternatives measured on the same clip: whisper-large-v3-turbo via the mlx-whisper already in the venv, 0.38 s warm, one error where Parakeet made two, but worse on Common Voice es (4.98) and English (6.36) and known to hallucinate on silence. Apple SpeechTranscriber (es-ES) 0.20 s, no Python, but garbled nearly every English term and has no language identification. Qwen3-ASR-1.7B perfect transcript at 3.8 s.
- No newer multilingual Parakeet exists. NVIDIA's 2026 releases are English-only Parakeet Unified and the streaming Nemotron 3.5 ASR (Spanish 4.23/6.91/5.16, below v3).
- Largest latency win is a Swift-native runtime for the same weights (FluidAudio CoreML, Apache 2.0, or mlx-audio-swift, MIT), which removes the Python spawn and the first-call warm-up.

### Meeting ASR

- Whisper large-v3 Spanish: FLEURS 2.30 (best of any open model), Common Voice 4.29, MLS 3.47. Long-form English 11.23 with CORAAL, 8.67 without.
- Canary-1B-v2 (Spanish 2.63/3.94/3.13, native word timestamps, 25 languages) is the closest replacement but requires the source language up front and has no auto detection. Runs through community MLX conversions in mlx-audio.
- Qwen3-ASR-1.7B is the only model beating Whisper on English (4.31) that also has auto language detection and a Spanish word aligner. Its Spanish average is 3.80, so it pays only for English-heavy meetings.
- Apple SpeechTranscriber: es_ES, es_MX, es_US, es_CL available on this Mac, word timing via audioTimeRange, vocabulary biasing via contextualStrings, no published WER, locale fixed per transcriber.
- No public benchmark exists for Spanish multi-speaker meetings or Spanish-English code-switching; every Spanish number above is read speech. The only zero-shot code-switching data point (CUI 2024, Bangor Miami corpus) puts fine-tuned Whisper variants at 44 to 76 WER.
- whispermlx is a single-maintainer WhisperX fork (14 releases since 2026-03, last push 2026-08-17) with no batching and only initial_prompt honored. mlx-audio 0.5.1 (2026-08-31) runs Whisper with DTW timestamps and every alternative above, so it is the one runtime for side-by-side tests on Brain's own recordings.

### Word alignment

- Native ASR timestamps lose to forced alignment in every primary comparison: on TIMIT, word boundary error is 19 ms MFA, 37 ms MMS-FA, 42 ms Whisper large-v3 cross-attention, 53 ms Voxtral, 80 ms Parakeet TDT (Zeyer, Schlüter, Ney, 2026-07). On AMI, stock Whisper DTW reaches F1 47.1 at 50 ms vs 63.5 for wav2vec2 alignment (Yeh et al., 2025-09). So the alignment stage stays.
- Qwen3-ForcedAligner-0.6B: 11 languages incl. es and en, 80 ms grid (wav2vec2 is 20 ms), 5 min per call (whispermlx aligns per segment, so not binding), MLX weights `mlx-community/Qwen3-ForcedAligner-0.6B-8bit`. Reported shift: es 36.8 ms, en 37.5 ms; wav2vec2 in whispermlx: es 108.0, en 92.1 (Qwen tech report Table 9, MFA-labeled).
- Fallback inside torchaudio: MMS_FA (1,130 languages, CC-BY-NC 4.0), 37 to 46 ms on TIMIT/Buckeye. whispermlx can load it with `--align_model MMS_FA` but does no romanization, so accented Spanish letters fall to the wildcard column; needs accent folding first.
- whispermlx 3.13.1 and upstream WhisperX 3.8.6 still ship the 2023 default aligners and offer nothing newer.

### Diarization and identification

- pyannote has not moved: 4.0.7 (2026-06-30) is the seventh bugfix release since 4.0.0 (2025-09-29). No open pyannote model in 2026. precision-2 is cloud-only. Two open PRs (#1992, #2048) claim 1.2x to 2.7x MPS speedups, unmerged.
- DiariZen clusters with the same wespeaker ResNet34-LM embedding community-1 uses, so speaker identification would be unchanged by the switch.
- NVIDIA Sortformer (v1, v2, v2.1) is capped at 4 speakers and English-trained. Nemotron-3-Diarization-preview (2026-08-24) is gated, evaluation-only, NVIDIA GPUs only.
- Joint ASR+diarization models with Spanish exist (MOSS-Transcribe-Diarize 0.9B, VibeVoice-ASR 8B, Trelis Tiron 2B) but emit segment-level anonymous labels, expose no speaker embedding, have no MLX runtime, and their AMI cpWER (28.6 to 34.7) does not beat a Whisper plus pyannote cascade. They do not remove the diarizer while cross-meeting identification is required.
- Verified locally: the vectors in speakers.json are responsibility-weighted means of raw 256-d WeSpeaker embeddings from non-overlapping speech, not PLDA-space. whispermlx ignores pyannote's exclusive_speaker_diarization but its max-overlap word assignment already collapses overlaps to one speaker.
- senko trails community-1 on every OpenBench dataset. FluidAudio's 10.6 percent AMI-SDM uses a 0.25 s collar with overlap ignored and is not comparable to pyannote's 19.9.

### Polish LLM

- Anthropic's placement: "start with Claude Opus 5 for most workloads. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5 at higher effort still fall short." Fable 5.1's lead over Opus 5 on knowledge work is 1853 vs 1824 on GDPval-AA v2.
- Effort: Anthropic documents xhigh for "long-running agentic and coding tasks (over 30 minutes)" and warns that a long single-request deliverable at xhigh or max may be drafted in thinking and written again. high is the documented starting point. On Opus 5, "use low and medium liberally as your primary control for token cost and response time wherever your evals show quality holds."
- Cursor's "NO ZDR" tag on Fable ids: inputs and outputs are stored by Anthropic for automated and human harm-prevention review, deleted after 30 days unless under investigation, regardless of Cursor Privacy Mode. Whether the Cursor CLI honors the account's Privacy Mode is not documented anywhere.
- Harnesses: `claude -p` adds a separate `--effort` flag and subscription billing but does not change retention. opencode documents only budgetTokens-style thinking, which Opus 5 rejects. Direct API costs about $1.70 per 30 min meeting at Opus 5 list price. No harness change is needed.
- Correction to the agent's note in `context/05-polish-llm.md`: the saved `.reasoning.jsonl` does contain thinking. The 433 KB file for one meeting holds 1,932 `thinking.delta` events carrying about 15k characters of summarized reasoning plus 129 assistant text events; the size is per-token JSON envelope overhead.
- Prompt edits to check in prompts/polish.md per the Opus 5 prompting guide: written documents run longer than on prior models (add a length instruction), and explicit verification instructions cause over-verification.

## Actions

Ordered by confidence and cost.

1. `scripts/polish_all.py`: change POLISH_MODEL and SUMMARY_MODEL from `claude-opus-5-thinking-xhigh` to `claude-opus-5-thinking-high`. Config change only.
2. Trial `claude-opus-5-thinking-medium` on three meetings and diff the polished output against thinking-high. Cuts the 6.5 min polish step if quality holds.
3. Align three recordings with Qwen3-ForcedAligner-0.6B via mlx-audio and compare word boundaries and speaker assignment against the current wav2vec2 output. Switch if boundaries are at least as good; drops torchaudio from the alignment stage.
4. Diarize the same recordings with DiariZen in a separate venv on CPU. Measure wall time and compare speaker turns against community-1. Switch only if the Mac CPU time is acceptable and the non-commercial license is acceptable for personal use.
5. Re-embed known speakers with ReDimNet2 B6 and compare cosine margins on the same recordings. Adopt if margins widen on compressed conferencing audio.
6. Benchmark Canary-1B-v2 and Apple SpeechTranscriber (es_ES) against Whisper large-v3 on the same recordings through mlx-audio and a small Swift harness. Only worth doing if the aligner switch lands first, since Canary's value is native timestamps.
7. Dictation: no model change. If latency matters more, move the Parakeet call to a Swift-native runtime (FluidAudio or mlx-audio-swift) and delete the Python spawn.

## Research status

- Phase: first-pass landscape complete, all claims cited to primary sources in the context files. No candidate has been run on a real Brain recording yet.
- Base materials: `context/01-dictation-asr.md`, `context/02-meeting-asr.md`, `context/03-alignment.md`, `context/04-diarization.md`, `context/05-polish-llm.md`.
- Local side effects of the dictation tests: Qwen3-ASR-1.7B (4.4 GB), Qwen3-ASR-0.6B (1.8 GB) and mlx-community/whisper-large-v3-turbo (1.5 GB) are in `~/.cache/huggingface/hub`; the Apple es-ES speech asset is installed system-wide; a scratch venv with mlx-qwen3-asr sits in the session scratchpad. Brain's venv was not modified.
- Open questions: Qwen3-ForcedAligner accuracy against human labels in Spanish; DiariZen CPU speed on Apple Silicon; any identification-embedding gain on compressed Teams audio; whether the Cursor CLI applies Privacy Mode.
