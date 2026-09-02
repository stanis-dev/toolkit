#!/usr/bin/env python3
"""Quick proof-of-concept: VibeVoice-ASR-HF on MPS with the oldest recording."""

import sys, os, time, json, gc, wave
import torch

WAV_FILE = sys.argv[1] if len(sys.argv) > 1 else "/Users/stan/code/toolkit/brain/data/rec-2026-03-24-152010.wav"
MODEL_ID = "microsoft/VibeVoice-ASR-HF"
DTYPE = torch.float16 if "--fp32" not in sys.argv else torch.float32
CHUNK_SIZE = 720000  # 30 seconds at 24kHz (default is 1440000 = 60s)

with wave.open(WAV_FILE) as wf:
    audio_dur = wf.getnframes() / wf.getframerate()

print(f"Model: {MODEL_ID}")
print(f"Dtype: {DTYPE}")
print(f"Chunk size: {CHUNK_SIZE} ({CHUNK_SIZE / 24000:.0f}s at 24kHz)")
print(f"Audio: {os.path.basename(WAV_FILE)} ({audio_dur:.0f}s / {audio_dur/60:.1f}min)")
print(f"MPS available: {torch.backends.mps.is_available()}")

from transformers import AutoProcessor, VibeVoiceAsrForConditionalGeneration

print(f"\nLoading processor...")
processor = AutoProcessor.from_pretrained(MODEL_ID)

print(f"Loading model ({DTYPE})...")
t0 = time.time()
model = VibeVoiceAsrForConditionalGeneration.from_pretrained(
    MODEL_ID, torch_dtype=DTYPE, low_cpu_mem_usage=True
).to("mps")
gc.collect(); torch.mps.empty_cache()
print(f"Model loaded in {time.time() - t0:.1f}s")

param_bytes = sum(p.numel() * p.element_size() for p in model.parameters())
print(f"Model memory: {param_bytes / 1e9:.2f} GB")

print(f"\nPreparing inputs...")
inputs = processor.apply_transcription_request(
    audio=WAV_FILE,
).to(model.device, model.dtype)
print(f"Input IDs shape: {inputs['input_ids'].shape}")

print(f"\nGenerating transcription (chunk_size={CHUNK_SIZE})...")
t0 = time.time()
with torch.no_grad():
    output_ids = model.generate(**inputs, acoustic_tokenizer_chunk_size=CHUNK_SIZE)
gen_time = time.time() - t0
print(f"Generation took {gen_time:.1f}s ({audio_dur/gen_time:.1f}x realtime)")

generated_ids = output_ids[:, inputs["input_ids"].shape[1]:]

raw = processor.decode(generated_ids, return_format="raw")[0]
print(f"\nRaw output length: {len(raw)} chars")

# Save immediately -- raw is always available regardless of parsing
out_path = WAV_FILE.rsplit(".wav", 1)[0] + ".vibevoice-test.json"
result = {"raw": raw, "gen_time": gen_time, "dtype": str(DTYPE), "chunk_size": CHUNK_SIZE}

try:
    parsed = processor.decode(generated_ids, return_format="parsed")[0]
    result["segments"] = parsed
    print(f"Parsed: {len(parsed)} segments")
except Exception as e:
    print(f"HF parsed decode failed ({e}), parsing raw JSON manually...")
    text = raw.strip()
    if text.startswith("<|im_start|>assistant"):
        text = text[len("<|im_start|>assistant"):].strip()
    parsed = json.loads(text)
    result["segments"] = parsed
    print(f"Manual parse: {len(parsed)} segments")

with open(out_path, "w") as f:
    json.dump(result, f, indent=2)
print(f"Saved to {os.path.basename(out_path)} ({os.path.getsize(out_path)} bytes)")

# Also write a human-readable .txt in the same format as the existing pipeline
txt_path = WAV_FILE.rsplit(".wav", 1)[0] + ".vibevoice-test.txt"
speakers = set()
lines = []
for seg in parsed:
    spk = seg.get("Speaker", "?")
    speakers.add(spk)
    start = seg["Start"]
    h, m, s = int(start // 3600), int((start % 3600) // 60), int(start % 60)
    ts = f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
    lines.append(f"[{ts}] Speaker {spk}: {seg['Content']}")
    lines.append("")

header = [f"Speakers: {len(speakers)}", ""]
with open(txt_path, "w") as f:
    f.write("\n".join(header + lines) + "\n")
print(f"Transcript saved to {os.path.basename(txt_path)} ({len(parsed)} segments, {len(speakers)} speakers)")

for seg in parsed[:5]:
    start = seg["Start"]
    m, s = int(start // 60), int(start % 60)
    spk = seg.get("Speaker", "?")
    txt = seg["Content"][:90]
    print(f"  [{m:02d}:{s:02d}] Speaker {spk}: {txt}")
if len(parsed) > 5:
    print(f"  ... and {len(parsed) - 5} more segments")
