#!/usr/bin/env python3
"""Dictation transcription using Parakeet via parakeet-mlx.

Launched at recording start so the model loads while the user speaks.
Protocol: prints "ready" when model is loaded, reads audio path from
stdin, prints transcription to stdout, then exits.
"""

import sys
from parakeet_mlx import from_pretrained

model = from_pretrained("mlx-community/parakeet-tdt-0.6b-v3")
print("ready", flush=True)

audio_path = sys.stdin.readline().strip()
if not audio_path:
    sys.exit(0)

try:
    result = model.transcribe(audio_path)
    text = (result.text or "").strip().replace("\n", " ")
    print(text, flush=True)
except Exception as e:
    print(f"ERROR: {e}", flush=True)
    sys.exit(1)
