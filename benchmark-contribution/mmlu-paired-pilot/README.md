# Tiny paired known-benchmark pilot — data retrieval BLOCKED

Selected proposal: MMLU test split, first5 rows each of clinical_knowledge and college_computer_science, source row indices0–4. This is clinical/CS multiple-choice knowledge, **not executable programming evaluation or clinical-use validation**. Tiny convenience prefix sample, not representative or leaderboard-equivalent. Public benchmark/pretraining contamination possible. No third domain needed.

Official reuse evidence: https://huggingface.co/datasets/cais/mmlu/blob/main/README.md declares MIT; https://github.com/hendrycks/test/blob/master/LICENSE is MIT (notice included, source blob fe20e951e94daaae0c02c070bad000ed85d1ad19). Official author README blob20d3d8d61dfcc1d02483155e7fdf40c47dfe4834 links https://people.eecs.berkeley.edu/~hendrycks/data.tar . Exact data version is NOT established because retrieval was denied. Do not substitute a guessed revision or source hash.

## Actual state

No benchmark source rows are ready. Retrieval from the author archive was rejected by auto-review. After parent supplied newer explicit user authorization and a nonmutating empty-directory/process check, one narrower10-row retry was also rejected. No further download route/retry is authorized in this task. Existing restriction must be resolved or authorized source rows supplied. Do not call this a completed benchmark, a data-backed pilot or synthetic replacement benchmark.

## Ready code

`python -m unittest -v` — seven passing offline SOFTWARE-FIXTURE tests. `python -m py_compile pilot.py` passed. No model/API calls, no generated-code execution, no paid resources.

`build(source)` consumes two groups `{archive_member, rows}` where each rows value contains exactly5 CSV rows `[question,A,B,C,D,gold_letter]`. It preserves source member, zero-based row index, item ID and source-row content SHA256. After authorized acquisition, preserve retrieval timestamp, archive/version identifier and source file hashes in a manifest; pin input before any model exposure. Keep gold tasks custodian-only.

`prompts(tasks)` returns paired prompt strings. Baseline and humor have byte-identical questions, choices, output contract and correctness instruction. Only commentary style differs: neutral/factual versus light wit without patient-directed mockery. No training/fine-tuning. Use the same verified model selector and fresh conversations, no tools/search/memory context, same available settings; record any UI settings that cannot be controlled. A new neutral task context per arm avoids carryover. Model UI may not disclose immutable checkpoints, so report the verified label and that limitation rather than inventing an API model ID.

Prefer four calls: clinical5 neutral, clinical5 humor, CS5 neutral, CS5 humor; alternate condition order across domains. Identical condition ordering is confounded by time; one paired run is a smoke pilot, not causal proof. These prompts can also be generated as10-item combined arms, but use separate subject batches for clear domain reporting. Record output receipts, observed latency, and cost as unknown unless verified. No paid API fallback is implied.

`evaluate(tasks, response)` checks exact JSON fields/IDs, rejects duplicates/unknown IDs, treats non-A–D answers as invalid, reports per-subject accuracy on all expected items and coverage. Missing predictions are not dropped from the denominator. Never grade humor from answer correctness: remove model/condition labels, randomize output IDs, and have independent humans rate commentary humor/safety/usefulness. Until then humor_score is null and no claim that the intervention actually made outputs funnier is valid.

CLI once data and genuine response exist:
`python pilot.py --tasks PRIVATE_TASKS.json --response REAL_RESPONSE.json`

No answers, source questions, raw model outputs or human labels are bundled. Existing general paired-domain scaffold retains checkpoint/config guards and paired task comparisons; this tiny adapter is for minimal known-benchmark intake/UI execution, not a replacement for a confirmatory study.
