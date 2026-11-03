# Paired same-model / multi-domain experiment

## What changed

The current question is not merely whether a model classifies jokes as funny. Compare:
1. **regular_baseline** — fixed regular checkpoint, no humor intervention;
2. **regular_humor** — exactly the same checkpoint and task settings, only the frozen humor harness changes;
3. OPTIONAL **frontier_baseline** — fixed frontier checkpoint, no humor intervention; not required for the primary paired experiment.

Run healthcare and programming independently with separate domain configurations/manifests and reports. Mixed-domain task files are rejected. A third domain is optional, not selected. The primary contrast is same-model humor minus same-model baseline, not a frontier comparison.

Measure deterministic task performance and human-perceived humor **separately**. The existing classification/rater work helps build a humor measure; it is not a substitute for the common task benchmark. Prior generation and classification artifacts remain provenance, not evidence of improvement.

## Runnable now, not a completed model benchmark

Standard library only; no network, packages, credentials, model calls, downloads or spend:

```sh
python -m unittest -v
python -m py_compile experiment.py test_experiment.py
```

Nineteen tests exercise synthetic SOFTWARE FIXTURES only. The arithmetic fixture in tests is not a proposed common benchmark and is not a heldout evaluation result. `empty-records.json` contains no predictions.

`config.UNSET.json` deliberately blocks evaluation until domain, benchmark ID/revision, regular immutable checkpoint ID (frontier may remain null), humor method/instruction and common decoding settings are selected and frozen. The implemented `exact_string_v1` scorer uses literal answer equality without trimming/case conversion; it is an adapter, **not a claim of compatibility with any established benchmark**. Choose an existing deterministic benchmark, confirm its license/official split/scorer, then implement/test its official scorer if different. Do not silently replace official evaluation formatting with this demo JSON contract.

## Experiment contract

1. Custodian obtains permitted benchmark heldout tasks and keeps answers out of requests and developer tuning artifacts. Development and heldout families must be disjoint; document overlap/pretraining-contamination limitations. This scaffold imports no task corpus or previous private heldout material.
2. Choose a common benchmark before inspecting outcomes. Freeze revision, item list, scoring normalization, sample size, model/provider version, decoding settings (temperature, token limit, seed support), timeout/retry policy, request order and repetition schedule. If a provider cannot implement common settings, disclose incompatibility; do not claim a controlled comparison. A single repeat is descriptive, not significance evidence.
3. Freeze the humor harness on development only. This version supports one extra instruction on the regular arm, not weight training. If the method later adds retrieval, reranking or multiple calls, revise and version the adapter and count **all** calls/latency/cost. No assumed improvement. A trained checkpoint would be a different experimental treatment and needs a revised protocol, not a silent checkpoint change.
4. `freeze(config, heldout_tasks)` hashes the config and full custodian task set, including answers. `requests(manifest, tasks)` creates two required otherwise identical task requests, plus frontier only if configured. Only regular_humor gets the additional intervention. The prompt/output contract and task hashes stay identical. Keep config and manifest unchanged. The frontier baseline is not tuned to outcomes.
5. Authorized operator runs requests and stores raw responses separately with immutable receipts. Records bind to the entire request hash (checkpoint/settings included). `actual_model_output:true` is a required operator attestation, **not independent proof**. Software fixture attestations in tests are not genuine runs. Request hashes do not verify a provider actually honored settings; receipts must supply that evidence.
6. `score(manifest, tasks, records)` reports exact task score, valid coverage, errors/missingness, observed latency and known cost subtotal. Unknown costs remain null; no account-plan or free-tier assumption. All-expected task score penalizes missing/error responses; conditional score is also shown. Matched comparisons use the same complete pair for each comparison; the primary pair never depends on optional frontier completion and report paired N, wins/losses/ties and signed accuracy differences. Inspect missingness before interpreting a delta; no confidence intervals or causal conclusion are supplied.
7. `blind_bundle(records, custodian_secret)` emits randomized opaque IDs plus a PRIVATE arm map. Custodian secret (at least16 characters), map, source receipts and task keys stay out of the public rater view. Rate all outputs, not only correct/funny-looking ones. Blinding cannot hide obvious stylistic clues; document that limit. Run records must first pass `score` validation.
8. Human rubric `humor-v1`: for a general adult English-speaking audience in a casual nonclinical setting, humor1=not amusing,2=slightly,3=moderately,4=very,5=exceptionally amusing. Separately mark safe and useful Boolean. Define usefulness relative to the task, not humor; safety concerns are not automatic unfunny labels. Use at least3 independently identified pseudonymous raters per output, same rubric and assignment procedure across arms. Allow refusal by leaving a rating absent; do not invent neutral votes. Record disagreements and rater coverage. Humans must not see model names/conditions before ratings.
9. Pass ratings through `score(..., humor_ratings=ratings)` for validation, then `humor_summary(ratings, private_map)` for equal-weight per-output averages only where>=3 raters. These averages are descriptive; compare the same item cohort across arms before claiming lift. Never use this utility's arm averages as an unpaired significance test. A positive humor change and negative task change is a tradeoff, not success by definition. Report whether the regular humor arm remains below/at/above frontier on the **task** metric without blending scores.

## Input schemas

Tasks (custodian only): `item_id,prompt,answer,split:"heldout",family_id,domain`, all nonempty strings. Unknown/duplicate fields fail. No such live file is bundled.

Run record: `arm,item_id,request_hash,actual_model_output,answer,commentary,latency_ms,cost_usd,cost_basis,error`. Answer/commentary may be null for invalid outputs; error may be null or error text. Preserve raw response elsewhere. Cost/latency may be null (unknown), never negative/nonfinite. Known cost needs a nonempty basis with provider price/retrieval date or receipt. Include retries in costs/latency according to the frozen policy.

Humor rating: `blind_output_id,rater_id,humor_1_to_5,safe,useful,rubric_version:"humor-v1"`. No source popularity, duplicate detector penalty or blank reviewer can become human gold.

## Verified repository context and limits

Collaborator inspected `kenn20/jokebench-rater-v2` main `de2febd0b6aedbac31a5b7436fe306c0fa18419f`: generator model names do not identify an agreed frontier/regular benchmark pair; no common deterministic task benchmark identified. Existing UI reveals model/condition and automatic duplicate penalties may populate funny=false. Keep its exported votes separate from independent blinded human ratings. This contribution neither copies team joke text nor imports private third-party exports.

No model IDs, benchmark or humor method selected by this scaffold. No real results, source rights grants, external uploads or claims of100-case completion. Integration belongs to the parent/factory worker.

## Adaptation boundary

This supersedes the earlier required-three-arm scaffold; that earlier folder is retained only for provenance. Domain and official benchmark selection remain unset. See BENCHMARK-OPTIONS.md for recommendations, not selected or downloaded corpora. The exact-string scoring implementation is ready for label tasks only after verifying the official scorer; it does NOT execute or score HumanEval code. That requires a separate reviewed sandboxed official-test adapter.
