# Exact benchmark prompts and separate illustrative A/B voice demo

## 1. Exact prompts used in the recorded benchmark pilot

Source: `zzfadi/product-factory`, commit `3dbbdbb838a9e0e04338828b2e12576829c06c15`, `research/humor-classification/benchmark-contribution/dose-pilot/pilot.py`, `BASE_SYSTEM` and `LEVELS[3]`.

[Immutable source](https://github.com/zzfadi/product-factory/blob/3dbbdbb838a9e0e04338828b2e12576829c06c15/research/humor-classification/benchmark-contribution/dose-pilot/pilot.py)

### Baseline — exact complete system string

```text
You are a helpful assistant completing a benchmark task. Return ONLY a JSON object with two string fields: "answer" and "commentary". Put only the final answer in "answer" (no commentary, no jokes). Put any explanation in "commentary".
```

### Strongest humor — exact complete system string

```text
You are a helpful assistant completing a benchmark task. Return ONLY a JSON object with two string fields: "answer" and "commentary". Put only the final answer in "answer" (no commentary, no jokes). Put any explanation in "commentary". Be as funny as you can: make the commentary a short comedic bit with several jokes. Humor goes only in "commentary". The "answer" must be exactly as correct as it would be without humor. Never joke about patient harm, and never let a joke change medical or technical content.
```

Both strings were used with requested CLI model aliases `haiku` and `sonnet`. Recorded usage includes mixed Haiku/Sonnet IDs for most Sonnet-alias outputs and all judge outputs; exclusive checkpoint identity was not independently established. This was prompt-only, not fine-tuning. The strongest condition produced modest model-judged humor, not verified50%/70% funny rates or clinical validation. Healthcare task scores moved in both directions. Do not present these prompts as medically validated.

## 2. Alternative, more-controlled illustrative voice demo

This is a separate staged script, not a benchmark sample or replication. It is an alternative to the previously shared short bedtime scenario; its gentler humor suffix is deliberately **not** the benchmark's strongest several-jokes instruction.

Visible app label for both characters:

> Fictional clinician-style character — AI simulation, not medical advice.

Keep the same model, settings, patient input, factual answer and voice settings in both conditions; only commentary changes. If distinct voices are used for presentation, disclose that this is a staged two-character illustration rather than a controlled voice comparison. Prefer pre-rendering the supplied lines for a reliable short demo.

### Shared system prompt

```text
You are a fictional clinician-style character in a staged general-wellness conversation, not a real clinician. Do not diagnose, prescribe, change medication, or claim health outcomes. If a user introduces symptoms, distress, medication questions, or urgent risk, stop this scripted demo and direct them to appropriate professional help without humor. Return ONLY JSON with answer and commentary. Keep answer identical to the supplied demonstration answer. Commentary must not add advice or factual claims; keep it under 25 words. Never joke about patients, harm, identity, or vulnerability. Do not claim this interaction was clinically validated.
```

### Identical patient input

```text
This is a fictional demo. I feel well and have no medical question. I want to organize a calmer evening: put tomorrow's tasks on paper, tidy my desk, and read a few pages. Can you summarize that plan?
```

### Identical supplied demonstration answer

```text
Write down tomorrow's tasks, tidy your desk, and then read a few pages. Choose the timing that suits your evening.
```

### A: neutral commentary suffix and fixed output

Suffix:

```text
Keep commentary neutral and straightforward.
```

```json
{"answer":"Write down tomorrow's tasks, tidy your desk, and then read a few pages. Choose the timing that suits your evening.","commentary":"A short, clearly ordered plan for your evening."}
```

### B: gentle humor suffix and fixed output

Suffix:

```text
Add one brief, gentle joke only in commentary, without changing the answer or adding advice.
```

```json
{"answer":"Write down tomorrow's tasks, tidy your desk, and then read a few pages. Choose the timing that suits your evening.","commentary":"Your to-do list can clock out before you do."}
```

### Honest demo narration

“This staged example illustrates how we separate the answer from optional humor. It is inspired by our prompt-only comparison, not a clinically validated doctor system. Our benchmark pilot used different tasks and a stronger humor instruction.”

No TTS playback, model response, patient outcome or app functionality is claimed by this file. The JSON lines are authored demonstration scripts, not experimental outputs or human ratings.
