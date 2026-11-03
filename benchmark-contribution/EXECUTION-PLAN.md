# Paired benchmark execution and contribution workflow

Owner direction, 2026-11-02: move quickly, all agents contribute through isolated Factory branches; dot validates and ports completed work to the existing team PR. Owner reviews the PR, not repeated planning messages. No main merge, competing writes, new access or unapproved spend.

## Entry points and actual status
- Factory entry: `zzfadi/product-factory`, branch `work/dot-humor-classification-2026-11-02`, receipt commit `e08e2b8ff6d87499506f7e3f6582855e844ec0e5`.
- Team delivery: https://github.com/kenn20/jokebench-rater-v2/pull/2 (draft), branch `contrib/dot-paired-benchmark-20261102`; verified head `c960ba93ff91eb07f9f74f8db85de5f290ac7bec`, base `ee62cb1d3b7df4c4ab4311fc0b0e411af78e5311`.
- Original contribution: 22 additive files, subtree `8413069fc96d0ef43de41d0ead85ad410031ba20`; later Factory documentation receipts intentionally differ.
- Completed: offline paired-request/scoring scaffold, 20 synthetic dev candidates, empty votes/runs, export auditor. 40 contribution unit tests pass. These are software tests, NOT model benchmarks. No primary experiment model run or human humor assessment exists yet. Existing team joke archives are separate descriptive experiments.

## Independent lanes and claims
| Lane | Owner/status | Bounded output | Completion evidence |
|---|---|---|---|
| Data and official scorer preparation | Active: dot's benchmark-data worker; do not duplicate | `benchmark-contribution/mmlu-paired-pilot/` (proposed integration path) | pinned official source/revision/license, permitted subset selection, scorer contract and tests, no answers in model requests |
| Integration and receipts | Active: dot; sole Mac executor handles team Git writes | this plan, validated imports, PR #2 updates | exact source commit/path/hash, required checks, remote head readback |
| Independent protocol review | Claimable after keeper/owner scope reconciliation | `research/humor-classification/reviews/<worker>/` | reproducible tests for matched tasks, arm isolation, missingness, domain separation; no live heldout inspection |
| Human humor annotation | Pending identified independent people | custodian-private ratings + sanitized aggregate receipt | at least 3 pseudonymous independent raters/output, blinded condition, coverage/disagreements recorded |
| Model execution | Pending frozen task/config and verified execution capability | own `research/humor-classification/runs/<run-id>/` sanitized receipt | untouched raw answers, actual model/settings evidence, request hashes, all failures/retries and observed latency/cost |

No lane grants new worker authority or overrides existing claims. New workers first read current main START-HERE/AGENTS/DISPATCH, claim their bounded own branch/path with a dated STATUS entry and base SHA. Never write another worker's branch. A waiting lane is not permission to fabricate labels or run a billable provider.

## Fastest honest pilot
Latest scope: the SAME model baseline versus multiple frozen humor-instruction levels on identical tasks; domains reported separately, with a possible third domain not yet selected. Targets such as 50%/70% funny are development calibration objectives, NOT guaranteed controls; baseline humor is measured too. Frontier remains optional. `humor-dose-response/` implements offline calibration guards and descriptive analysis; it is not calibrated or run. Improvement is a hypothesis; preserve negative/zero changes.

1. Data worker pins a permitted established benchmark revision and official scorer. Prefer a small, predeclared label-task pilot first; do not equate the demo exact-string scorer with HumanEval code execution. Programming execution needs a separately reviewed sandbox and official tests; do not execute model-generated code on the host.
2. Freeze model identity, task IDs, sample size, instruction, output schema, decoding controls, arm order and retry policy BEFORE viewing outcomes. Select separately for each domain. Current `config.UNSET.json` intentionally blocks scoring until required fields are set.
3. Use only an already authorized, verified execution route. Existing team `generate-v2.mjs`/`generate-v3.mjs` call a paid-capable external API; no included/free allowance was established from source. Do not run them as tests. The v3 generator uses different assigned premises across arms, not a matched-task common benchmark.
4. Latest owner direction: do the work ourselves; do NOT use Gemini unless later needed. No model runtime is currently verified for no-charge execution from inspected team source. Use only a separately verified existing local model/runtime or an authorized provider allocation with actual billing limits established before calls. Do not invent an immutable checkpoint or free quota. No account-plan details belong in shared artifacts.
5. Run the matched pair on the frozen permitted tasks; no selecting only good/funny responses. Report task accuracy, all-expected coverage, complete-pair N/wins/losses/ties, and humor ratings separately. Unknown costs stay null. No significance/causality claim from a tiny pilot.

## Schemas and reproducibility
Canonical schemas/functions are in `paired-domain/README.md` and `experiment.py`: `freeze(config,tasks)`, `requests(manifest,tasks)`, `score(manifest,tasks,records)`. This is an importable Python module, not an invented CLI. `config.UNSET.json` is the template. Task answers remain custodian-side; requests must omit them. Records bind to request hashes and retain actual-output attestation, answer/commentary/error, latency and cost basis. Attestation is not independent provider verification.

A delivery receipt must state: worker/base/commit/path allowlist; input source URLs/revisions/licenses and hashes; config/task/request hashes; actual execution route and observed identity/settings limitations; original raw-output artifact hash; scorer/version/command; expected/attempted/completed/invalid counts; all retries; results or explicit not-run status. Keep secrets, private customer/team exports, annotation identities, heldout keys and maps out of Git. A public benchmark's legal reuse does not make its answers tune-facing material.

## Exact Factory → team workflow
1. Worker delivers only own bounded Factory branch; append own STATUS and SOURCES, run ALL current Factory gates plus affected tests, state DONE/BLOCKED with exact commit and file list through existing repository routes. No direct competing team push.
2. Dot reads actual remote files/diff, checks provenance/privacy, verifies hashes and tests, reconciles latest main/claims, rejects fabricated outputs or leaked keys. No blind cherry-pick of Factory history into the team repository.
3. Sole team integration executor refreshes Kenn main and PR #2 head, preserves teammate changes, copies approved files only. Mapping: `research/humor-classification/benchmark-contribution/` → `benchmark-contribution/`. Reviews outside that subtree require an explicit sanitized mapping before porting. Do not copy Factory STATUS/SOURCES/operational records wholesale.
4. Run team gates and component tests below; inspect exact staged diff. Commit to existing PR branch, normal non-force push, verify remote commit/diff/checks and update PR #2. Do not create duplicate PRs or merge. If access/gates fail, retain patch and report exact blocker without bypass.
5. Record resulting team commit/PR and tests on own Factory handoff. Owner reviews the coherent PR. Only concrete deliveries or essential decisions warrant user interruption.

```sh
npm test
python3 scripts/validate-fireworks-archive.py
python3 -m unittest discover -s benchmark-contribution -p test_team_export_audit.py -v
(cd benchmark-contribution/humor-classification && python3 -m unittest -v)
(cd benchmark-contribution/paired-domain && python3 -m unittest -v)
git diff --cached --check
```

Factory gates remain those in FACTORY.md: SPI Node tests, build_spi, factory check, govern, income_check, secret scan, factory/governance tests, plus every affected component. No blanket invocation of provider generation scripts, frozen assets or live services.

## Current data-worker handoff
Worker reports a proposed 5 + 5 MMLU clinical_knowledge / college_computer_science pilot. This is healthcare and computer-science MULTIPLE-CHOICE KNOWLEDGE, not an executable programming benchmark; do not relabel it as HumanEval-equivalent. Worker verified official MIT evidence, but actual archive retrieval was denied by approval review and stopped; no benchmark rows have been acquired by that lane. No retry or alternate import route is authorized by this plan. Offline strict A–D scorer/prompt builder is being prepared against synthetic fixtures; actual import needs resolved approval or an explicitly authorized supplied bounded input. Preserve this blocked state until actual evidence changes.

## Remaining choices, not invented defaults
Official benchmark revision/split/scorer and permitted pilot subset; actual model/execution route; fixed humor method; settings/retries/sample size; human raters. Data/scorer preparation and independent review can proceed now. Actual benchmarking starts only when the corresponding input and execution conditions are established. No model performance is claimed by this plan.

## Offline dose-response component delivered
`humor-dose-response/` has 13 synthetic tests, no calibration receipt or actual runs. It separates target from observed funny rates and reports per-domain paired task counts/deltas, humor coverage and descriptive intervals. Human calibration must use development-only outputs and independent blinded votes. Keep task-test outcomes out of tuning; do not treat declared calibration hashes/flags as independent proof. Interval caveats are in its README. The paired-domain and tiny pilot components remain distinct, not automatically wired together; task request/receipt/scorer provenance must be checked at integration.
