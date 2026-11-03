# Benchmark transfer contribution — preparation, not results

Additive contribution refreshed against team main `3918cafabde557a07c007952038ba458ad89e614`, preserving the newly merged Fireworks archive. Initial source review was at `de2febd0b6aedbac31a5b7436fe306c0fa18419f`. Existing rater, generator, dataset and UI are unchanged. No model/API calls were made. No credentials or private account details are included.

## Two evaluation tracks
1. **Common deterministic benchmark:** compare a fixed regular baseline and the same exact model with a frozen humor intervention, with an OPTIONAL frontier reference on identical benchmark items/settings. Exact model IDs, benchmark/version and intervention are not yet selected. Improvement is a hypothesis, not an expected outcome; negative transfer is possible.
2. **Humor:** measure whether the intervention improves humor separately, with independent blinded raters and predeclared scoring. Classification against human votes and judging generated jokes are distinct tasks. Never claim that making a model funnier necessarily improves a general benchmark.

`humor-classification/` contains 20 original synthetic development candidates and a strict offline scorer with empty votes/runs. It is not a completed benchmark, contains no heldout texts and cannot establish model performance.

## Audit existing team rating exports

```sh
python3 benchmark-contribution/team_export_audit.py PATH_TO_EXPORTED_JSON --reviewer-id PSEUDONYM
python3 -m unittest discover -s benchmark-contribution -p test_team_export_audit.py -v
```

The audit separates explicit timestamped vote records from automatic originality penalties, requires an operator-provided pseudonymous reviewer ID and does not produce gold labels. It does not verify the person or independence. Keep real individual ratings private; this contribution contains none.

## Source observations (not alterations)
- Existing generator specifies `z-ai/glm-5.3-flash`, `nvidia/nemotron-3.5-lightning`, `deepseek/deepseek-v4.1-flash`. These are inspected configuration strings, not independently verified availability, pricing or frontier/baseline selections for the new experiment.
- Current 60-row dataset has two automatic originality-penalty `funny=false` entries and no explicit timestamped votes. They are not human humor ground truth.
- Current rater exposes model/condition and writes a blank reviewer field. Blinding and reviewer identity are not established by its export.
- Generator writes an 80-item file including human harness examples, while README, app and test target a different 60-item generated-only file. No regeneration was attempted.
- Upstream has no AGENTS.md or license file in the inspected tree. No blanket third-party dataset reuse rights are inferred. Original contribution provenance is separate.

## Validation and execution boundaries
Run upstream `npm test` plus the contribution tests. `npm run generate:v2` and the generation shell scripts are not tests: they call a paid-capable external provider and were NOT run. No server, deployment or fork was performed. Delivery is verified through the authorized Mac route: draft PR https://github.com/kenn20/jokebench-rater-v2/pull/2, head c960ba93ff91eb07f9f74f8db85de5f290ac7bec, base main ee62cb1d3b7df4c4ab4311fc0b0e411af78e5311. Exactly 22 added files and no deletions; no main merge. Earlier connector write limitations are historical, not a current delivery blocker. Do not merge or overwrite teammates' paths.

Use a fresh heldout version if evaluation items or labels influence tuning. Preserve failed/invalid outputs and missing submissions; keep unknown costs unknown. Report actual model/version, item/config hashes and all intervention latency/cost when runs exist.

## Paired-domain scaffold

`paired-domain/` includes the frozen-request protocol, exact-string adapter, complete-case task deltas, separate blinded humor workflow and 19 synthetic unit tests. Run `(cd benchmark-contribution/paired-domain && python3 -m unittest -v)`. Configuration is deliberately unset; do not mistake the arithmetic software fixture or exact-string adapter for an established selected benchmark. The initial method supports an added instruction, not fine-tuning. Blind bundles omit errors and null commentary: disclose those exclusions and coverage, never claim all outputs were human-rated.

The updated upstream Fireworks archive contains separate human sessions and descriptive scores. It is preserved unchanged; these are not runs of this new paired-domain experiment. Its validator passed (8 datasets, 4 unique sessions), without independently verifying the raters or external provider execution.

Primary domains are healthcare and programming, reported separately. Frontier is optional and never controls primary-pair completeness. Benchmark recommendations are not selections or imported corpora.

Factory receipt update only: the PR contains the original validated 22-file snapshot (subtree 8413069fc96d0ef43de41d0ead85ad410031ba20). This later receipt wording has not been pushed to the team branch. No remote status checks or Actions runs were present at verification; pending aggregate with zero checks is not a pass. Models/benchmarks/intervention remain unset and no model benchmark has run.
