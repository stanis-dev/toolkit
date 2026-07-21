---
name: sierra-debug
description: Critical guidance for Sierra agent debugging. Use every time you need to find why an agent failed.
---

1. Find the earliest turn agent steered from ideal path. Symptoms to look for:

- A condition gating context over/under triggered.
- A tool received wrong tool params or returned wrong results.
- A tag failed to trigger or unwanted one fired.

2. Preset your finding is simple language - what happened vs what should have happened and where the most elegant fix
   likely lies.
