# Speaker diarization and speaker identification, state as of 2026-09-04

Scope: the local meeting pipeline (Whisper large-v3 via whispermlx, then `pyannote/speaker-diarization-community-1` on pyannote.audio 4.0.7, device mps, return_embeddings, cosine match at 0.75 against speakers.json). Sources are model cards, repos, changelogs and vendor docs only. Every number carries its URL.

## Verdict

1. One open local diarizer is verified ahead of community-1 on the same protocol (no collar, overlap scored): DiariZen `BUT-FIT/diarizen-wavlm-large-s80-md-v2` (Dec 2025) reports AMI-SDM 13.9 vs 19.9, DIHARD3 14.5 vs 20.2, VoxConverse 9.1 vs 11.2, AliMeeting 10.8 vs 20.3, and lands within a point of the cloud-only precision-2 on most sets. Costs: weights are CC BY-NC 4.0, the code picks cuda or cpu (no mps branch), torch is pinned to 2.1.1 (separate venv), and it clusters with the same wespeaker ResNet34-LM embedding community-1 uses, so speaker identification would be unchanged.
2. pyannote itself has not moved: pyannote.audio 4.0.7 (2026-06-30) is the last of seven bugfix releases since 4.0.0 (2025-09-29); no open pyannote model was published in 2026; precision-2 stays API-only (self-hosting is Enterprise-only). Two open PRs (#1992, #2048) claim 1.2x to 2.7x speedups on MPS but are unmerged.
3. NVIDIA Sortformer (offline v1, streaming v2, v2.1) is capped at 4 speakers and trained mostly on English; the new `nvidia/Nemotron-3-Diarization-preview` (2026-08-24) is gated under an evaluation-only license restricted to NVIDIA GPUs. None fits 2 to 8 Spanish speakers on a Mac.
4. Open joint ASR+diarization models now exist with Spanish (MOSS-Transcribe-Diarize 0.9B, Apache 2.0; Microsoft VibeVoice-ASR 8B, MIT; Trelis Tiron 2B, Apache 2.0) but they emit segment-level anonymous speaker labels, expose no speaker embedding, have no MLX runtime, and their published cpWER on AMI (28.6 to 34.7) does not beat a Whisper + pyannote cascade on evidence I could find. They do not remove the separate diarizer while cross-meeting identification is a requirement.
5. The identification embedding is the cheapest thing to upgrade: community-1 embeds with a WeSpeaker ResNet34 (256-d, roughly 0.8 percent EER on VoxCeleb1-O). ReDimNet2 B6 (0.29 percent, MIT, 12.3M params, 2026-07-01), ReDimNet B6 (0.40 percent) and WeSpeaker ResNet293-LM (0.425 percent) cut verification error by half or better on the standard benchmark. The 0.804 match against a 0.75 threshold in the recent run shows how thin the current margin is. Gain on compressed Teams audio is unverified.

## Comparison table

| System | Date | Type | Max speakers | DER or EER (dataset, protocol) | Spanish | Apple Silicon runtime |
|---|---|---|---|---|---|---|
| pyannote community-1 (current) | 2025-09-29 | standalone diarizer (segmentation + WeSpeaker ResNet34 + VBx) | no hard cap (min/max params) | DER AMI-SDM 19.9, AMI-IHM 17.0, DIHARD3 20.2, VoxConverse 11.2, AliMeeting 20.3, CALLHOME 26.7 (no collar, overlap scored, automatic speaker count) [1] | language-agnostic | PyTorch mps, ~60 s per 30 min on M4 Max (observed) |
| pyannoteAI precision-2 | 2025-09 | cloud diarizer + voiceprint identification | Live-1 variant caps at 8; batch not stated | DER AMI-SDM 15.6, AMI-IHM 12.9, DIHARD3 14.7, VoxConverse 8.5, AliMeeting 15.2, CALLHOME 16.6 (same protocol as above) [1] | language-agnostic | none (API; self-host only on Enterprise) [7] |
| DiariZen WavLM-Large-s80-md-v2 | 2025-12-09 | standalone diarizer (pruned WavLM Large EEND + wespeaker ResNet34-LM + VBx) | up to 4 overlapping at once; total not capped | DER AMI-SDM 13.9, DIHARD3 14.5, VoxConverse 9.1, AliMeeting 10.8, MSDWild 15.8, RAMC 11.0, AISHELL-4 10.1 (no collar) [10][11] | trained on English + Mandarin corpora; not stated | code selects cuda else cpu; torch 2.1.1 pinned [12][13] |
| NVIDIA diar_sortformer_4spk-v1 | 2024-12 | end-to-end offline diarizer | 4 | DER DIHARD3 (<=4 spk) 16.28 no collar; CALLHOME 2spk 6.49 / 4spk 14.14 with 0.25 s collar [15] | primarily English, "may degrade on non-English" | NeMo + CUDA only |
| NVIDIA diar_streaming_sortformer_4spk-v2.1 | 2025-10-22 | end-to-end streaming diarizer | 4 | DER DIHARD3 (<=4 spk) 15.09, AMI 16.67 to 20.57, AliMeeting far 15.60 at 1.04 s latency; v2 on DIHARD3 5 to 9 spk: 42.2 [16][17] | primarily English | mlx-audio port `mlx-community/diar_streaming_sortformer_4spk-v2.1-fp16`; CoreML port in FluidAudio [18][19] |
| NVIDIA Nemotron-3-Diarization-preview | 2026-08-24 | streaming-sortformer family (tags) | not readable (gated) | none published | not readable | evaluation license, NVIDIA GPUs only [20] |
| senko | commits to 2026-08-27 | standalone diarizer (pyannote segmentation-3.0 + CAM++ + clustering) | not stated | DER VoxConverse 13.5 to 17.7, AMI-IHM 26.5 to 27.5, AMI-SDM 29.7 to 32.8, AliMeeting 30.4 to 31.4 (OpenBench, collar 0, overlap scored) [21][22] | language-agnostic | CoreML on ANE; 1 h in 7.7 s on M3 |
| FluidAudio offline (community-1 CoreML port) | v0.15.6 2026-08-19 | standalone diarizer (same models as community-1) | as community-1 | DER AMI-SDM 10.6 but with collar 0.25 and overlap ignored, not comparable to pyannote's 19.9 [23][24] | language-agnostic | Swift/CoreML, 323x real time on M5 Pro; no Python API |
| FluidAudio LS-EEND | 2026 | streaming end-to-end diarizer | 10 | DER AMI-SDM 20.7 (collar 0.25, overlap ignored) [24] | not stated | Swift/CoreML, CPU-only path 74x on M4 Max |
| 3D-Speaker / FunASR CAM++ pipeline | last news 2024-12 | cascaded diarizer | not stated | DER AISHELL-4 10.30, VoxConverse 11.75 (protocol not stated) [25] | Mandarin/English training | PyTorch, ONNX |
| Mistral Voxtral Mini Transcribe V2 | 2026-02-04 | joint ASR + diarization (API) | not stated | none published for diarization | yes (13 languages) | none; the open Voxtral-Mini-4B-Realtime-2602 has no diarization [27][28][29] |
| ElevenLabs Scribe v2 | 2026-01-09 | joint ASR + diarization (cloud) | 32 | none published for diarization | yes (90+ languages) | none [30][31] |
| NVIDIA multitalker-parakeet-streaming-0.6b-v1 | 2025 | ASR with speaker tags fed by Streaming Sortformer | 4 (inherited) | cpWER AMI-IHM 21.26, AMI-SDM 37.44 | English only | NeMo + CUDA [32] |
| MOSS-Transcribe-Diarize 0.9B | 2026-07-09 | joint ASR + diarization, open weights Apache 2.0 | not stated; 90 min single pass | cpCER AISHELL-4 15.83, AliMeeting 22.17; cpWER AMI 28.61 (Trelis eval) [33][35] | yes (50+ languages) | transformers / vLLM / SGLang; no Mac runtime documented |
| Microsoft VibeVoice-ASR 8B | paper 2026-01, transformers 2026-03 | joint ASR + diarization, MIT | not stated; 60 min single pass | AMI WER 17.20; DER/cpWER only as charts [34] | yes (50+ languages) | transformers v5.3+; no Mac runtime documented |
| Trelis Tiron 2B | 2026-07-21 | joint ASR + diarization (Whisper large-v3 based), Apache 2.0 | 8 per meeting | cpWER AMI 34.68, ICSI 21.24, NOTSOFAR-1 36.23 [35] | via Whisper language tokens | transformers on CUDA/MPS/CPU, 3 to 12 GB |
| WeSpeaker ResNet34-LM (what community-1 wraps) | 2023 | embedding | n/a | EER VoxCeleb1-O 0.797 (LM), 0.723 (LM + AS-norm) [37] | language-agnostic | PyTorch mps (inside pyannote) |
| WeSpeaker ResNet293-LM | 2023 | embedding | n/a | EER VoxCeleb1-O 0.425 (LM + AS-norm + QMF), 28.6M params [37] | | PyTorch |
| SpeechBrain ECAPA-TDNN | 2021 | embedding | n/a | EER VoxCeleb1 cleaned 0.80 [38] | | PyTorch |
| NVIDIA TitaNet-large | 2022 | embedding | n/a | EER VoxCeleb1 cleaned 0.66, 23M params [39] | English training | NeMo |
| 3D-Speaker CAM++ | 2023 | embedding | n/a | EER VoxCeleb1-O 0.65, 7.2M params [25] | | PyTorch, ONNX, CoreML (senko) |
| ReDimNet B6 | 2024-07 | embedding | n/a | EER VoxCeleb1-O 0.40, 15.0M params (vox2, ft_lm) [40] | | torch.hub |
| ReDimNet2 B6 | 2026-07-01 | embedding, MIT | n/a | EER VoxCeleb1-O 0.29 / E 0.52 / H 0.99, 12.3M params [41] | | torch.hub |

## Per-candidate notes

### pyannote (current setup)

What community-1 is made of. The pipeline config in the local HF cache (`~/.cache/huggingface/hub/models--pyannote--speaker-diarization-community-1/snapshots/3533c8cf.../config.yaml`) reads: segmentation `$model/segmentation`, embedding `$model/embedding`, `clustering: VBxClustering`, `plda: $model/plda`, `embedding_exclude_overlap: true`, thresholds `threshold 0.6, Fa 0.07, Fb 0.8`. Loading the bundled embedding checkpoint with torch shows architecture `pyannote.audio.models.embedding.wespeaker.WeSpeakerResNet34`, 6,642,884 parameters, output layer `resnet.seg_1` of shape (256, 5120), so 256-d embeddings computed on 5 s chunks. That parameter count and dimension match WeSpeaker's `ResNet34-TSTP-emb256` (6.63M params) [37]. The model card cites the WeSpeaker paper for the embedding and Plaquet and Bredin 2023 for the powerset segmentation [1]. Whether the weights are byte-identical to `pyannote/wespeaker-voxceleb-resnet34-LM` [36] is not verifiable from the card.

What return_embeddings returns. In pyannote.audio 4.0.7 `VBxClustering.__call__` computes `centroids = W.T @ train_embeddings / W.sum(0).T` where `train_embeddings` are the raw 256-d WeSpeaker embeddings and `W` are the VBx responsibilities; the PLDA transform is applied only to a copy (`fea = self.plda(train_embeddings)`) used for the VBx step (local file `.venv/lib/python3.13/site-packages/pyannote/audio/pipelines/clustering.py`, lines 555 to 670; same code on develop [3]). So the vectors stored in speakers.json are responsibility-weighted means of raw WeSpeaker embeddings, computed from non-overlapping speech only (`embedding_exclude_overlap: true`), not L2-normalized. Cosine matching against them is in the same space as any `pyannote/wespeaker-voxceleb-resnet34-LM` embedding, which is what DiariZen also uses [13]. When the pipeline forces the speaker count with k-means, centroids become plain means over hard clusters (same file).

Benchmark protocol. The community-1 card states the DER table is "fully automatic processing, no forgiveness collar, nor skipping overlapping speech", last updated 2025-09 [1]. Full table (legacy 3.1 / community-1 / precision-2): AISHELL-4 12.2 / 11.7 / 11.4; AliMeeting ch1 24.5 / 20.3 / 15.2; AMI IHM 18.8 / 17.0 / 12.9; AMI SDM 22.7 / 19.9 / 15.6; AVA-AVD 49.7 / 44.6 / 37.1; CALLHOME pt2 28.5 / 26.7 / 16.6; DIHARD 3 21.4 / 20.2 / 14.7; Ego4D 51.2 / 46.8 / 39.0; MSDWild 25.4 / 22.8 / 17.3; RAMC 22.2 / 20.8 / 10.5; REPERE 7.9 / 8.9 / 7.4; VoxConverse 11.2 / 11.2 / 8.5 [1]. Argmax's independent OpenBench run of community-1 (2025-09-29) gives 0.11 VoxConverse, 0.18 AMI-IHM, 0.21 AMI-SDM, 0.22 DIHARD-III, 0.23 AliMeeting, 0.30 CallHome, consistent with the card [22].

Changes since 4.0.0 (CHANGELOG [2]). 4.0.0 (2025-09-29): VBx clustering replaces agglomerative, exclusive speaker diarization output, torchcodec replaces torchaudio for I/O, pyannoteAI SDK wrapper, offline cloning, optional telemetry (`PYANNOTE_METRICS_ENABLED`), Python 3.10 minimum, sox/soundfile backends removed. 4.0.1 (2025-10-10): warn instead of raise on unsupported diarization arguments. 4.0.2 (2025-11-19): `Binarize` returns string tracks (breaking), torch/torchcodec/torchaudio pinned to avoid a segfault (torchcodec issue 995), pyannoteAI wrapper returns exclusive diarization too, `Pipeline.cuda()`, `preload` option, directory CLI. 4.0.3 (2025-12-07): `--revision` CLI option, `Calibration.safe_transform`, lightning 2.6 fix. 4.0.4 (2026-02-07): relaxed torch constraints, SpeechBrain embedding auth fix. 4.0.5 (2026-06-22): fewer telemetry packets, `--average-case` optimize option. 4.0.7 (2026-06-30): `subfolder` support in `Pipeline.from_pretrained`, basic sequential batch inference. No 4.1. The HF API lists no `pyannote/*` model created in 2026; the newest are community-1 (created 2025-04-15, modified 2025-09-29), `speaker-diarization-precision-2` and `speaker-diarization-community-1-cloud` (both 2025-09-13, API stubs) [4]. The `pyannoteAI` org hosts only Parakeet and faster-whisper mirrors [5].

Exclusive diarization. `DiarizeOutput.exclusive_speaker_diarization` is built by capping the instantaneous speaker count to 1 before reconstruction ("speaker diarization adapted to downstream transcription (does not contain overlapping speech turns)") [3]. whispermlx 3.13.1 `diarize.py` reads only `output.speaker_diarization` and `output.speaker_embeddings`, never the exclusive one, and assigns each word to the speaker with the largest overlap duration via an IntervalTree, with a nearest-segment fallback [6]. Net effect: overlapping words already collapse to one speaker, chosen by overlap duration rather than by pyannote's "most likely to be transcribed" rule.

precision-2 and identification. The pyannoteAI models page describes precision-2 as "28% more accurate than Community-1 on average", with voiceprint identification, exclusive mode, confidence scores, API-based, "self-hosted options available on Enterprise plans"; Live-1 streams with up to 8 speakers [7]. Identification uses voiceprints from single-speaker samples of at most 30 s, a 0 to 100 threshold, and opaque encoded voiceprint strings (no raw vector exposed) [8]. `pyannote/speaker-diarization-precision-2` on HF is a stripped SDK that runs on pyannoteAI cloud with an API key [9].

MPS in 2026 (GitHub). PR #1992 (opened 2026-03-12, still open at last update 2026-04-23): the stock code routes FFT to CPU on MPS, `repeat_interleave` pre-materializes chunk x speaker (58.8 GB for a 4.7 h, 21-speaker file), fixed 16 GB budget; measured 1.17x end-to-end and 4.46x on the FFT step on an M2 Max [42]. PR #2048 (opened 2026-08-14, open): one embedding forward per chunk instead of one per (chunk, speaker); claims 2.4x to 2.7x whole-pipeline on an M3 with MPS and identical DER (7.18 percent on every VoxConverse file) [43]. PR #2051 (same idea) was closed as a duplicate on 2026-08-27 [44]. Issue #1886 (2025-06-21) is a training-only MPS crash on M4, marked wontfix [45]. Local observation: the brain venv's torchcodec cannot load (FFmpeg dylibs missing, pyannote prints a warning), but whispermlx passes audio as an in-memory `{"waveform", "sample_rate"}` dict (`diarize.py` line 137), so decoding never goes through torchcodec and the run is unaffected.

### DiariZen (BUT Speech@FIT)

Repo latest commit 2026-08-04 ("docs: install torch via pip instead of conda; add constraints.txt") [14]; README news 2026-01-31 adds multi-channel WavLM [10]. Models: `BUT-FIT/diarizen-wavlm-base-s80-md`, `-large-s80-md`, `-large-s80-md-v2` (v2 collection update 2025-12-09) [11]. Architecture: WavLM Large + Conformer local EEND, structurally pruned at 80 percent sparsity to 63.3M parameters and 3.8G MACs/s, "supports up to four overlapping speakers" per local window, trained on AMI, AISHELL-4, AliMeeting, NOTSOFAR-1, MSDWild, DIHARD3, RAMC, VoxConverse far-field single-channel audio [11]. Clustering via pyannote's `SpeakerDiarization` pipeline with `pyannote/wespeaker-voxceleb-resnet34-LM` embeddings and VBx by default [13]. README DER table (no collar, no per-dataset adaptation), pyannote 3.1 / Base-s80 / Large-s80 / Large-s80-v2: AMI-SDM 22.4 / 15.8 / 14.0 / 13.9; AISHELL-4 12.2 / 10.7 / 9.8 / 10.1; AliMeeting far 24.4 / 14.1 / 12.5 / 10.8; NOTSOFAR-1 none / 20.3 / 17.9 / 16.7; MSDWild 25.3 / 17.4 / 15.6 / 15.8; DIHARD3 full 21.7 / 15.9 / 14.5 / 14.5; RAMC 22.2 / 11.4 / 11.0 / 11.0; VoxConverse 11.3 / 9.7 / 9.2 / 9.1 [10]. Their pyannote 3.1 column is within 0.3 points of pyannote's own 3.1 numbers on AMI-SDM, DIHARD3 and VoxConverse [1], so the two tables are comparable. Runtime: `inference.py` picks `cuda:0` if available else `cpu` [13]; constraints.txt pins torch 2.1.1, torchvision 0.16.1, torchaudio 2.1.1, numpy 1.26.4 [12]; the repo ships a modified pyannote-audio [10]. Licenses: code MIT, weights CC BY-NC 4.0 [10]. An M4 Max CPU run time is not published.

### NVIDIA Sortformer family

`diar_sortformer_4spk-v1` (HF created 2024-12-09): 123M params, offline, max 4 speakers ("performance degrades on recordings with 5 and more speakers"), trained on 2,030 h real + 5,150 h simulated, primarily English, CC-BY-NC-4.0, roughly 12 min max on a 48 GB GPU; DER DIHARD3-eval (<=4 spk) 16.28 no collar, CALLHOME-part2 2/3/4 spk 6.49/10.01/14.14 with 0.25 s collar, overlap included [15]. `diar_streaming_sortformer_4spk-v2` (2025-06-04): 117M, streaming, 4 speakers, DIHARD3 1 to 4 spk 14.49, DIHARD3 5 to 9 spk 42.22, CALLHOME 2spk 7.51, CC-BY-4.0, "primarily English" [16]. `diar_streaming_sortformer_4spk-v2.1` (2025-10-22): same cap, more meeting data (AMI, ICSI, AISHELL-4, DIHARD), DIHARD3 <=4 spk 15.09, AliMeeting near/far 12.60/15.60, AMI 16.67 to 20.57 at 1.04 s latency, NVIDIA Open Model License [17]. Apple Silicon: `mlx-community/diar_streaming_sortformer_4spk-v2.1-fp16` runs through `mlx_audio.vad.load(...).generate_stream(...)`, no speed or accuracy numbers given [18]; FluidAudio ships a CoreML port and measured 31.7 percent DER on AMI-SDM (collar 0.25, overlap ignored) at 126x on an M2 [24]. `nvidia/Nemotron-3-Diarization-preview` (created 2026-08-24, modified 2026-08-29) is gated with manual approval, tagged streaming-sortformer and speaker-tagging, under the NVIDIA Software and Model Evaluation License: internal test and evaluation only, no production, NVIDIA GPUs only [20]. `multitalker-parakeet-streaming-0.6b-v1` adds speaker tags to ASR but needs Streaming Sortformer's output (so 4 speakers), runs one model instance per speaker, English datasets only, cpWER AMI-SDM 37.44 [32]. The NeMo diarization models page (updated 2026-04-13) lists no model above 4 speakers [46].

### senko

Latest commit 2026-08-27 [21]. Pipeline: pyannote segmentation-3.0 (or Silero VAD) plus CAM++ embeddings plus clustering; on macOS VAD and embeddings run through CoreML on the ANE, fbank and clustering on CPU; 1 h of audio in 7.7 s on an M3; MIT [21]. Evaluation uses Argmax OpenBench defaults (`collar=0.0`, `skip_overlap=False`) [21]: DER AISHELL-4 0.133 to 0.136, AMI-IHM 0.265 to 0.275, AMI-SDM 0.297 to 0.328, AliMeeting 0.304 to 0.314, Earnings-21 0.209 to 0.211, ICSI 0.375 to 0.378, VoxConverse 0.135 to 0.177, AVA-AVD 0.713 to 0.722 [21]. OpenBench's community-1 row on the same tool: AISHELL-4 0.12, AMI-IHM 0.18, AMI-SDM 0.21, AliMeeting 0.23, Earnings-21 0.10, ICSI 0.35, VoxConverse 0.11, AVA-AVD 0.48 [22]. senko trails community-1 on every dataset; its advantage is speed. README lists limitations: degrades with noise, similar voices merge, one speaker across two microphones splits [21].

### FluidAudio (CoreML, Swift)

v0.15.6 published 2026-08-19; the last five releases (June to August 2026) added a CAM++ embedding backend, FSMN-VAD, per-chunk embeddings on DiarizationResult, deterministic VBx re-clustering, and a prepare()/cluster() split [23]. Offline pipeline = "powerset segmentation + WeSpeaker + VBx" (community-1 port); LS-EEND streaming up to 10 speakers with 100 ms updates; Sortformer streaming limited to 4 [26]. Benchmarks.md (Apple M5 Pro, 2026-07-03): offline DER 10.6 percent on the 16-meeting AMI-SDM test split with collar 0.25 and `ignoreOverlap=True`, 323x real time, 12 of 16 meetings with the right speaker count; LS-EEND 20.7 percent at 74x on an M4 Max CPU path; Sortformer 31.7 percent [24]. Their claim that 10.6 "matches published pyannote-community-1 offline numbers on this split (~11-12%)" refers to a collar-forgiving protocol, not pyannote's 19.9 no-collar figure [1][24]. Swift only; React Native and Rust wrappers; no Python bindings [26]. Speaker enrollment and embedding extraction are exposed for identification [26].

### 3D-Speaker and FunASR

3D-Speaker README: last news entry 2024-12 (diarization recipes and benchmark results); verification EER on VoxCeleb1-O: CAM++ 0.65 (7.2M), ERes2Net-large 0.52 (22.46M), ERes2NetV2 0.61 (17.8M), ECAPA-TDNN 0.86, ResNet34 1.05; diarization DER AISHELL-4 10.30, VoxConverse 11.75 (collar/overlap not stated); Apache 2.0 [25]. FunASR exposes the same CAM++ as `spk_model="cam++"` next to a Chinese Paraformer, returning segment-level speaker labels; the speaker model is documented for Chinese [47]. Nothing new in 2026 in either repo.

### Joint ASR + diarization

Mistral Voxtral Transcribe 2 (announced 2026-02-04): Voxtral Mini Transcribe V2 (batch, API, $0.003/min) does "speaker labels and precise start/end times" plus word-level timestamps in 13 languages including Spanish; "with overlapping speech, the model typically transcribes one speaker" [27]. The docs enable it with a `diarize` parameter on `voxtral-mini-latest`; no num_speakers parameter or max speaker count is documented [29]. The open-weights model `mistralai/Voxtral-Mini-4B-Realtime-2602` (Apache 2.0, 4B, 13 languages) is transcription only, no speaker labels [28]. Diarization therefore is cloud-only.

ElevenLabs Scribe v2 (2026-01-09): cloud, up to 32 speakers, word-level timestamps, 90+ languages with Spanish rated "Excellent (<= 5% WER)", realtime variant at ~150 ms; no diarization accuracy metric published [30][31].

OpenMOSS `MOSS-Transcribe-Diarize` 0.9B (2026-07-09): Apache 2.0, 50+ languages including Spanish, single pass up to 90 min, output format `[start][Sxx]text[end]` (segment-level anonymous labels), cpCER AISHELL-4 15.83, AliMeeting 22.17, Podcast 7.37, Movies 12.76 against Doubao, ElevenLabs, GPT-4o, Gemini and VibeVoice; transformers with remote code, vLLM, SGLang; no max speaker count, no Mac runtime documented [33]. Trelis's evaluation lists MOSS-TD cpWER AMI 28.61, ICSI 21.84, NOTSOFAR-1 25.86 [35].

Microsoft `VibeVoice-ASR-HF` (paper arXiv 2601.18184, in transformers v5.3+, HF doc): 8B, MIT, 50+ languages including Spanish, 60 min in one pass within 64K tokens, JSON segments with Speaker, Start, End, Content; Open ASR Leaderboard WER 7.77, AMI WER 17.20; DER and cpWER shown only as charts; audio tokenized at 24 kHz in 60 s chunks [34].

Trelis `tiron` (2026-07-21): Whisper large-v3 derivative, 2B BF16, Apache 2.0, 30 s windows with up to 8 speakers per window and 8 global speakers per meeting, segment-level labels with 20 ms timestamps, cross-window linking with an external ECAPA embedding, runs via transformers on CUDA, MPS or CPU in 3 to 12 GB at ~43x real time; cpWER AMI 34.68, ICSI 21.24, NOTSOFAR-1 36.23 (worse than MOSS-TD on AMI and NOTSOFAR-1) [35]. Spanish only through Whisper language tokens; not evaluated.

Others checked: Qwen3-ASR (2026-01-29) has no built-in diarization; the FunASR and MLX wrappers bolt CAM++ or pyannote on [48]. Kyutai's 2026 releases (Pocket TTS, Hibiki-Zero) contain no diarization model [49]. TagSpeech (arXiv 2601.06896, code under AudenAI/Auden) is a research recipe on AMI/AliMeeting without a packaged model [50]. No Meta or Google open joint model surfaced.

### Speaker embedding models for cross-meeting identification

WeSpeaker VoxCeleb recipe (vox1-O / E / H EER): ResNet34-TSTP-emb256 (6.63M) 0.867 / 1.049 / 1.959 baseline, 0.797 / 0.937 / 1.695 with large-margin fine-tuning, 0.723 / 0.867 / 1.532 with AS-norm; ResNet221-LM 0.505 / 0.676 / 1.213; ResNet293-LM + AS-norm + QMF 0.425 / 0.641 / 1.146 (28.62M); ECAPA-TDNN c1024 0.707 / 0.894 / 1.615; CAM++ 0.659 / 0.803 / 1.569; ReDimNet2 B6 0.330 / 0.502 / 0.985 [37]. WeSpeaker's pretrained list includes `voxceleb_resnet34_LM` (HF `Wespeaker/wespeaker-resnet34-LM`) and `ReDimNet2B6_LM` [51]. `pyannote/wespeaker-voxceleb-resnet34-LM` is "a wrapper around WeSpeaker wespeaker-voxceleb-resnet34-LM" for pyannote.audio 3.1+, CC-BY-4.0 [36]. SpeechBrain `spkrec-ecapa-voxceleb`: 0.80 EER on VoxCeleb1 test cleaned, Apache 2.0 [38]. NVIDIA `speakerverification_en_titanet_large`: 0.66 EER on VoxCeleb1 cleaned, 23M params, English-heavy training, CC-BY-4.0 [39]. ReDimNet EVALUATION.md (vox2, ft_lm): B2 0.57, B3 0.50, B5 0.43, B6 0.40 on vox1-O [40]. ReDimNet2 (PalabraAI/redimnet2, Interspeech 2026, weights released 2026-07-01, MIT): B3 0.42 (4.1M), B5 0.33 (8.9M), B6 0.29 / 0.52 / 0.99 (12.3M), loadable via torch.hub [41].

Reading for the pipeline: the stored profiles are means of 256-d WeSpeaker ResNet34 embeddings; the recent 0.804 similarity against a 0.75 threshold is a small margin for a 2 to 8 speaker meeting mix. A stronger model (ReDimNet2 B6 or ResNet293-LM) would be run as a second pass over each speaker's non-overlapping segments (the diarization output gives the timestamps), producing a separate profile space; the existing speakers.json vectors would need re-enrollment. Every EER above is on read English VoxCeleb audio; none of the cards report results on compressed conferencing audio or Spanish.

## What I could not verify

- Whether the embedding weights bundled inside community-1 are identical to `pyannote/wespeaker-voxceleb-resnet34-LM`; only the architecture (WeSpeakerResNet34), parameter count (6.64M) and 256-d output were checked locally.
- Any DER for community-1, DiariZen or senko on Spanish or on compressed Teams/Meet audio; all cited sets are English or Mandarin meeting and telephone corpora.
- DiariZen speed on Apple Silicon (its code has no mps branch; CPU timing is not published).
- Nemotron-3-Diarization-preview specs (speaker cap, DER, languages); the README is behind manual gating.
- precision-2's DER table beyond the community-1 card; the pyannoteAI docs give only "28% more accurate than Community-1".
- The benchmark protocol behind 3D-Speaker's diarization numbers and FluidAudio's assertion that pyannote publishes ~11 to 12 percent on AMI-SDM under a collar.
- Word-level speaker attribution quality of MOSS-Transcribe-Diarize, VibeVoice-ASR and Tiron; all three publish cpWER/cpCER, none publish a Spanish figure, and none run under MLX.
- Whether PRs #1992 and #2048 will be merged; both were open at last fetch.
- pyannoteAI per-minute pricing (billing page defers to the dashboard plans page).

## Sources

[1] https://huggingface.co/pyannote/speaker-diarization-community-1
[2] https://github.com/pyannote/pyannote-audio/blob/develop/CHANGELOG.md
[3] https://github.com/pyannote/pyannote-audio/blob/develop/src/pyannote/audio/pipelines/speaker_diarization.py
[4] https://huggingface.co/api/models?author=pyannote&sort=lastModified&direction=-1&limit=30
[5] https://huggingface.co/api/models?author=pyannoteAI
[6] https://github.com/KalebJS/whispermlx/blob/main/whispermlx/diarize.py
[7] https://docs.pyannote.ai/models.md
[8] https://docs.pyannote.ai/tutorials/identification-with-voiceprints.md
[9] https://huggingface.co/pyannote/speaker-diarization-precision-2
[10] https://github.com/BUTSpeechFIT/DiariZen
[11] https://huggingface.co/BUT-FIT/diarizen-wavlm-large-s80-md-v2
[12] https://github.com/BUTSpeechFIT/DiariZen/blob/main/constraints.txt
[13] https://github.com/BUTSpeechFIT/DiariZen/blob/main/diarizen/pipelines/inference.py
[14] https://api.github.com/repos/BUTSpeechFIT/DiariZen/commits?per_page=1
[15] https://huggingface.co/nvidia/diar_sortformer_4spk-v1
[16] https://huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2
[17] https://huggingface.co/nvidia/diar_streaming_sortformer_4spk-v2.1
[18] https://huggingface.co/mlx-community/diar_streaming_sortformer_4spk-v2.1-fp16
[19] https://huggingface.co/Alkd/Sortformer-Diarization-CoreML/blob/main/README.md
[20] https://huggingface.co/nvidia/Nemotron-3-Diarization-preview and https://huggingface.co/api/models/nvidia/Nemotron-3-Diarization-preview
[21] https://github.com/narcotic-sh/senko and https://github.com/narcotic-sh/senko/tree/main/evaluation
[22] https://github.com/argmaxinc/OpenBench/blob/main/BENCHMARKS.md
[23] https://api.github.com/repos/FluidInference/FluidAudio/releases?per_page=5
[24] https://github.com/FluidInference/FluidAudio/blob/main/Documentation/Benchmarks.md
[25] https://github.com/modelscope/3D-Speaker
[26] https://github.com/FluidInference/FluidAudio
[27] https://mistral.ai/news/voxtral-transcribe-2/
[28] https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602
[29] https://docs.mistral.ai/studio/audio/speech_to_text/offline_transcription
[30] https://elevenlabs.io/docs/capabilities/speech-to-text
[31] https://elevenlabs.io/blog/introducing-scribe-v2
[32] https://huggingface.co/nvidia/multitalker-parakeet-streaming-0.6b-v1
[33] https://huggingface.co/OpenMOSS-Team/MOSS-Transcribe-Diarize
[34] https://huggingface.co/microsoft/VibeVoice-ASR-HF and https://huggingface.co/docs/transformers/model_doc/vibevoice_asr
[35] https://huggingface.co/Trelis/tiron
[36] https://huggingface.co/pyannote/wespeaker-voxceleb-resnet34-LM
[37] https://github.com/wenet-e2e/wespeaker/blob/master/examples/voxceleb/v2/README.md
[38] https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb
[39] https://huggingface.co/nvidia/speakerverification_en_titanet_large
[40] https://github.com/IDRnD/ReDimNet/blob/master/EVALUATION.md
[41] https://github.com/PalabraAI/redimnet2
[42] https://github.com/pyannote/pyannote-audio/pull/1992
[43] https://github.com/pyannote/pyannote-audio/pull/2048
[44] https://github.com/pyannote/pyannote-audio/pull/2051
[45] https://github.com/pyannote/pyannote-audio/issues/1886
[46] https://docs.nvidia.com/nemo-framework/user-guide/latest/nemotoolkit/asr/speaker_diarization/models.html
[47] https://github.com/modelscope/FunASR
[48] https://github.com/QwenLM/Qwen3-ASR and https://huggingface.co/Qwen/Qwen3-ASR-1.7B/discussions/24
[49] https://kyutai.org/blog/
[50] https://arxiv.org/abs/2601.06896
[51] https://github.com/wenet-e2e/wespeaker/blob/master/docs/pretrained.md
