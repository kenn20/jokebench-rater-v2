# Same-model humor dose-response — offline component

Latest direction: do the work ourselves; **do not use Gemini unless later needed**. No model/API execution, paid calls or dataset retrieval occurs here. The denied MMLU data acquisition remains stopped; this component neither retries nor embeds a corpus. Previous frozen pilot adapter is untouched.

## What50% /70% means

A target funny rate is a **calibration objective**, not a model capability setting or guaranteed outcome. Configured low/medium examples target0.50/0.70; high remains unset rather than inventing a requested percentage. Baseline humor is measured too, not assumed zero. Conditions need not achieve targets or even monotonic observed humor. The null-checkpoint config is an uncalibrated candidate, not a frozen experiment.

Define funny rate as fraction of independently rated outputs judged funny by a strict majority of at least3 distinct blinded human raters under `binary_humor_v1`. Each rater answers: "Would a general adult English-speaking audience in a casual nonclinical setting find this output amusing?" true/false/null(unsure or decline). Abstentions count toward majority denominator, never become false votes. Record safety/usefulness separately in the broader rater workflow; do not infer them from funniness. This component's binary votes only measure humor, not clinical appropriateness.

## Development calibration → freeze → task test

1. Use only a disjoint development HUMOR set to adjust low/medium/high instructions. No task-test questions, scores or heldout humor examples may guide tuning. Preserve all attempted conditions, prompts, receipts, votes and cost, not just the best-looking outputs. Choose a finite calibration budget and stopping rule before calls. If targets are unattained within that budget, freeze best available conditions and disclose observed rates—do not keep tuning on the task test.
2. Preserve a calibration artifact and SHA256. `freeze(config, task_ids_by_domain, calibration_receipt)` requires a nonempty checkpoint/decoding config, development-only declaration and no test exposure. These are **operator attestations**, not independent verification. A SHA or Boolean does not prove the experiment occurred. No actual receipt is bundled.
3. Pin model checkpoint/provider version, decoding, task benchmark revision/scorer, item/sample IDs, common task/output contract, sample count, repeat schedule and call-order randomization. Keep identical items/settings across all conditions. Use one manifest per frozen intervention experiment, distinct task IDs per domain. Never vary model weights while calling it a same-checkpoint prompt intervention. Code-generation scoring needs its approved sandbox/official scorer; this component consumes deterministic results and never executes generated code.
4. `requests(manifest,prompts)` rejects changed manifests and mismatched IDs. It produces one request per item/condition with the same checkpoint, decoding and task; only the condition instruction changes. The execution owner must preserve raw outputs, request hashes and receipts, enforce identical settings and account for all retries/multicalls.
5. Blind condition/model IDs before human review. After freezing, collect humor ratings of actual task outputs as a manipulation check—not to retune. Analyze every assigned output, not just the funny subset. Archive task-test access before any later development revision; revised interventions require a new independent test set.

## Analysis

`analyze(manifest, records, votes)` reports per domain and condition:
- expected/recorded/valid counts, task accuracy over the full expected denominator;
- target funny rate versus observed funny rate, resolved humor count and coverage;
- Wilson95 interval for the observed funny proportion;
- paired task difference from baseline on available scored pairs, paired N, descriptive normal95 interval;
- observed latency mean/count, known cost subtotal and null total if any cost/missing run remains unknown.

Missing or failed deterministic scores use task_correct=null; do not replace unknown scores with fabricated correct/incorrect labels. The expected-denominator accuracy is accompanied by coverage to expose failures. Pairwise complete-case comparisons can still suffer missingness bias. The small-sample normal interval can degenerate at zero variance and is not confirmatory; show raw paired counts and do not claim significance from it. Wilson intervals assume independent items; shared raters, repeated samples and clustered prompts break that assumption. A confirmatory study needs cluster-aware uncertainty/repeat design and multiple-comparison control across levels/domains.

Plot observed humor (with interval/count) versus task delta **separately per domain**, label target levels as targets, not achieved x-axis values. Do not automatically fit a line or causal dose curve. Prompt intensity is assigned; observed humor is an outcome and may correlate with task difficulty. This distinguishes an assigned-condition effect from an observational humor/performance association. No pooled healthcare/programming score or claimed universal optimum.

Records strict fields: condition,item_id,manifest_sha256,actual_model_output,task_correct,output_id,latency_ms,cost_usd. A true actual_model_output flag is operator attestation; verify against raw receipts before reporting. Votes strict fields: output_id,rater_id,funny,blinded,rubric. Store blind mapping privately; the analysis receives resolved mappings only after ratings lock.

## Validation

`python -m unittest -v` runs13 synthetic SOFTWARE-FIXTURE tests; `python -m py_compile dose.py test_dose.py`. Fixture votes/outputs are not humans/models and never benchmark evidence. No real results, datasets, keys or access changes are bundled. Integration allowlist is in MANIFEST.json.
