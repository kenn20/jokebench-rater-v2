# Recorded dose-pilot: independent result audit

Source commit: `3dbbdbb838a9e0e04338828b2e12576829c06c15`. No provider calls, new dataset retrieval or generated code execution during audit.

In this tiny recorded pilot, stronger humor instructions produced modest model-judged humor; healthcare accuracy changed in both directions, while recorded coding scores remained at ceiling.

| Requested model alias | Domain | Baseline | Strongest | Delta | Paired W/L/T | Strongest funny >=3 (model judge) |
|---|---|---|---|---|---|---|
| haiku | healthcare | 30/40 (75%) | 29/40 (72.5%) | -2.5pp | 2/3/35 | 9/40 (22.50%) |
| haiku | programming | 30/30 (100%) | 30/30 (100%) | +0pp | 0/0/30 | 4/30 (13.33%) |
| sonnet | healthcare | 29/40 (72.5%) | 33/40 (82.5%) | +10pp | 4/0/36 | 3/40 (7.50%) |
| sonnet | programming | 30/30 (100%) | 30/30 (100%) | +0pp | 0/0/30 | 2/30 (6.67%) |

## Verified
560 unique task records,560 unique model judgments,70 unique task IDs. Every model/level/domain uses the identical domain item set; zero request-hash mismatches against source prompt/settings. All stored healthcare scores match independent lowercase/trimmed label comparison. Reported counts/accuracy reconcile.56 raw strings require the documented fence/brace recovery; none fail after recovery. Judge JSON matches all stored humor/safety fields.

## Do not overclaim
- One repeat;40healthcare and30coding items per arm; public possibly memorized tasks.
- Strongest-condition observed model-judged funny rate spans6.67–22.5%;50/70% targets not achieved.
- Haiku healthcare declined2.5percentage points; do not say humor never hurt.
- Sonnet healthcare +10points is4wins0losses on40pairs; exact two-sided sign test p=.125, exploratory multiple comparisons.
- Programming30/30 every arm: ceiling and custom unreviewed subprocess tests, not independent official-harness reproduction.
- Humor and safety are single model-judge stand-ins, not human panel or clinical safety validation.
- Prompt-only intervention, no fine-tuning or demonstrated dose calibration.
- No inference that a simulated patient/two-doctor TTS demo is clinical evidence.

Model identity caveat: CLI `modelUsage` keys list both Haiku and Sonnet on278of280 Sonnet-alias outputs and every judge output. These records alone do not show which model produced final text. Label requested aliases unless richer execution receipts establish identity.

Cost: stored task-call list estimates sum$3.19207462; judge estimates$4.8594934; total$8.05156802. These are not independently verified charges or permission to spend.

Source: https://github.com/zzfadi/product-factory/blob/3dbbdbb838a9e0e04338828b2e12576829c06c15/research/humor-classification/benchmark-contribution/dose-pilot/results.json

Suggested spoken headline: “We tested four humor instructions on the same tasks. Our small pilot produced modest model-rated humor—not the50or70percent targets. Medical-answer scores moved in both directions; coding scores were already at ceiling. This is a feasibility result, not proof that humor improves accuracy.”
