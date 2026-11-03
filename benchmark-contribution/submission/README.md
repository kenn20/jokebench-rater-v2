# Humor without sacrificing task performance? A descriptive pilot and reproducible toolkit

## Submission status
This combines dot's validated offline experiment toolkit with another worker's **recorded model pilot**, preserved with immutable provenance. The pilot is not a simulation according to its source records, but our verification is of recorded data, request consistency and arithmetic—not independent observation of provider execution, billing or secure code execution. No new model calls or dataset retrieval were performed for this submission. This packet is review material for the existing team PR, not a merge or public submission receipt.

## What the pilot supports
Source: [Factory commit 3dbbdbb](https://github.com/zzfadi/product-factory/commit/3dbbdbb838a9e0e04338828b2e12576829c06c15), authored Claude (coauthor Claude Opus 5.5). Recorded design: 40 PubMedQA questions + 30 HumanEval tasks, two requested model aliases, four prompt humor levels, one repeat = **560 task records** and 560 model-judge records.

| Requested alias / domain | Plain | Strongest humor | Paired W/L/T | Interpretation |
|---|---:|---:|---:|---|
| Haiku / PubMedQA | 30/40 (75%) | 29/40 (72.5%) | 2 / 3 / 35 | −2.5 percentage points; not universal improvement |
| Sonnet / PubMedQA | 29/40 (72.5%) | 33/40 (82.5%) | 4 / 0 / 36 | +10 points in this tiny sample; descriptive, not established benefit |
| Haiku / HumanEval | 30/30 (100%) | 30/30 (100%) | 0 / 0 / 30 | ceiling; cannot discriminate improvements |
| Sonnet / HumanEval | 30/30 (100%) | 30/30 (100%) | 0 / 0 / 30 | ceiling; cannot discriminate improvements |

The source README's blanket “did not hurt” headline is too strong: some healthcare arms declined. Sonnet level1 is 28/40 (70%), down from 29/40. Do not present the strongest-arm bump as a general causal result. Four discordant wins and zero losses have two-sided exact sign-test p=0.125, before any multiple-comparison consideration.

## Humor metric: observed, not targeted
One Sonnet-alias model judge assigned amusement1–5 and a safety flag. “Funny” means judge score ≥3. This is **not human-verified humor**, nor our separate majority-human rubric. Maximum observed rate is 9/40 (22.5%); the pilot does not reach 50% or 70%. Baseline humor is measured, not assumed. Assigned prompt level and achieved humor are different variables. Zero recorded unsafe flags mean only that this judge flagged none—not a safety validation.

The source also reports a correctness/safety-gated “humor credit.” That is a composite secondary metric, not pure humor; use task accuracy and raw model-judged humor separately in the main presentation.

## Provenance and limitations that must travel with the chart
- Requested aliases are haiku and sonnet. Haiku task records list `claude-haiku-5-5`; 278 of280 Sonnet-alias records list BOTH `claude-haiku-5-5` and `claude-sonnet-5-5` in usage metadata; two list Sonnet only. All560 judge records list both IDs. These receipts do not uniquely establish the model that generated each answer. No immutable same-checkpoint guarantee is inferred.
- Source reports existing `claude -p` execution, default temperature (not controllable), tools/MCP off, 4096 output-token cap, thinking off, fresh process, randomized arm order. We did not independently inspect the runtime or replay calls.
- Public benchmarks may be memorized. PubMedQA uses first40 questions in file order; HumanEval uses a fixed30-task rule. These are convenience subsets, not representative full-benchmark scores.
- HumanEval correctness flags came from the source worker's unreviewed local subprocess harness, NOT a verified secure official execution environment. We did not execute generated code. The source runner is archived as `pilot.py.txt` for inspection only; do not run it or copy its subprocess strategy into production.
- Source lists task-call cost estimates totaling $3.19207462 and judge estimates $4.8594934, total $8.05156802. These are list-price estimates, not verified charges, zero-cost evidence or permission for further calls.
- Single judge, self-model judging possible, truncated judge task/response context, no independent human votes, one repeat, tiny N and multiple arms. No universal optimum, significant uplift, clinical-use safety or frontier-equivalence claim.
- Source task answers/tests are archival evaluation material. Do not use them to tune interventions and then claim an independent heldout evaluation.

## Our reusable contribution
The surrounding `benchmark-contribution/` contains strict development classification and export auditing; paired-domain request/scoring and provenance; a blocked-input tiny MMLU intake adapter; and development-calibrated humor dose-response analysis. These are original offline scaffolds with synthetic unit tests, not extra model measurements. MMLU data acquisition remains stopped; this separate worker's PubMedQA/HumanEval records do not authorize retrying it. No private heldout/customer data or account details are included.

## Review and integration
`SOURCE-MANIFEST.json` records exact source commit, paths, Git blobs and SHA256s. Source files are preserved unchanged except runner filename; the source README remains an attributed historical claim, superseded by this wrapper where qualified. Official MIT notices for PubMedQA and HumanEval are included. Independent audit artifacts are RESULTS-AUDIT.md and audited-summary.json: 560 unique records/judgments, identical item sets, zero reconstructed request-hash mismatches and all healthcare label scores verified. Coding flags are aggregated without execution. Run `python3 validate_submission.py` for the safe archival hash/count/healthcare check. Dashboard is a separately delivered static view of this same audited data; no dashboard presence is claimed until its artifact is verified.

All workers deliver isolated Factory branches; dot validates and the sole integration executor ports completed files to **existing Kenn PR #2**. No competing team writes, duplicate PR or main merge. Preserve raw records and failed outputs; future studies need development-only calibration, independent human humor labels, harder uncontaminated tasks and a verified safe execution/budget route.
