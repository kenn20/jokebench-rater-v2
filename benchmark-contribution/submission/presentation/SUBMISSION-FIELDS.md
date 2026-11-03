# Submission field draft — review before entry

Prepared 2026-11-02 23:57 UTC. Unsubmitted. Exact authenticated form labels remain unverified: public project route required login. Do not sign in through cloud on this task; use the user's selected Mac route. No terms accepted, upload, save, or submission performed.

## Paste-ready core

**Working project title:** Killing Joke — Humor Without Losing the Task

**Short description:** A reproducible pilot testing whether stronger humor instructions can coexist with task performance, with a separate simulated-patient voice demonstration.

**Overview:** We tested four humor instruction levels on the same 40 healthcare question-answering and 30 programming tasks using two requested Claude model aliases, producing 560 task records and 560 model judgments. The intervention was prompt-only, not fine-tuning. The pilot found modest model-rated humor, mixed healthcare accuracy changes, and coding scores already at ceiling. We preserve raw outputs, prompts, settings, paired comparisons and limitations. A separate simulated-patient comparison illustrates baseline versus humor-adapted doctor dialogue with TTS; it is a demonstration, not clinical evidence.

**Intended user / proposed value:** Builders exploring conversational style adaptation while retaining task quality. This pilot helps identify where humor may hurt performance and where further controlled evaluation is required. Patient communication is an illustrative use case only; patient outcomes, trust, adoption, time savings and clinical safety were not measured.

**Approach:** Four prompt conditions, fixed shared task cases, deterministic task scoring where applicable, and a separate single-model humor/safety judge. Requested aliases must not be presented as conclusively verified final model identities. No model training or fine-tuning is established.

## Audited task-pilot results

Source audit: `../humor-results-audit/RESULTS-AUDIT.md`; source commit `3dbbdbb838a9e0e04338828b2e12576829c06c15`.

| Requested alias | Task | Baseline | Strongest humor instruction | Difference | Paired W/L/T | Strongest model-judged funny >=3 |
|---|---|---:|---:|---:|---|---:|
| haiku | Healthcare | 30/40 (75%) | 29/40 (72.5%) | -2.5 pp | 2/3/35 | 9/40 (22.5%) |
| sonnet | Healthcare | 29/40 (72.5%) | 33/40 (82.5%) | +10 pp | 4/0/36 | 3/40 (7.5%) |
| haiku | Programming | 30/30 | 30/30 | 0 pp | 0/0/30 | 4/30 (13.33%) |
| sonnet | Programming | 30/30 | 30/30 | 0 pp | 0/0/30 | 2/30 (6.67%) |

560 unique task records and 560 unique judgments cover 70 unique tasks, not 560 independent cases. One repeat. Same cases across conditions. Healthcare scores independently reconciled; 56 output strings needed documented fence/brace parsing recovery. Programming uses custom unreviewed subprocess tests, not independently reproduced official-harness results. Public tasks may be memorized. Sonnet-alias +10 pp is four wins, no losses across 40 pairs; exploratory two-sided sign test p=.125. Humor targets of 50%/70% were not achieved. Humor/safety scores are model judgments, not human or clinical validation.

**Identity limitation:** CLI modelUsage reports both Haiku and Sonnet in 278/280 Sonnet-alias task outputs and all judge outputs. These records do not establish the final responding model. Use requested aliases until richer receipts resolve this.

**Cost:** Stored estimates total $8.05156802 (tasks $3.19207462; judgments $4.8594934), not independently verified billing. No measured cost advantage or latency advantage is established here.

## Separate JokeBench human pilot — never combine denominators

Public team repository inspected at `ee62cb1d3b7df4c4ab4311fc0b0e411af78e5311`: published human jokes 16/20; preference-guided GLM 15/20; minimal GLM 10/20; minimal GPT-OSS 9/20. Four unique human sessions / 80 votes. Different joke sets, one unblinded reviewer per set, adaptive selection and shared reviewer preferences mean descriptive results only. This is not the 560-record task pilot and not proof of causal improvement or frontier superiority.


## Required fields/assets still to resolve

- **Final public submission repository:** PENDING team choice. Current team repo https://github.com/kenn20/jokebench-rater-v2 . Task-pilot source currently resides in product-factory; final single reviewable repo must include or clearly link approved evidence and reproducible instructions.
- **Judged commit hash:** PENDING final consolidated commit; do not use this document's inspected commits as automatically selected submission versions.
- **Video:** PENDING final accessible link/upload, verified duration <120 seconds, completed processing.
- **Patient app:** Owned and handled separately by the user. Not a dependency for this benchmark/slides work; do not request its owner/link again or duplicate the build.
- **Team roster:** PENDING accepted project roster and all contributors. Fadi Al Zuabi, Kenn Chong and Moses Rajan are observed participants, not independently verified complete accepted roster.
- **Sponsor tracks:** PENDING team choice and documented relevant technology. Fireworks JokeBench archive demonstrates Fireworks use, but do not relabel Claude task calls as Fireworks execution. Published cash and NVIDIA prize cards require Fireworks.
- **AI / prior-work disclosure:** Material assistant use and pre-existing code/data must be disclosed; identify event-specific contributions. Include source attribution and applicable licenses. Do not claim ownership of published jokes.

## Required frontier evidence gap

Official rules require an OPEN-MODEL system compared against a NAMED FRONTIER baseline on the SAME cases. The two-Claude-alias task pilot alone is not that open-versus-frontier experiment. The separate different-joke human pilot also does not establish it. Unless additional audited same-case open-versus-frontier results arrive, explicitly report the gap; do not claim 'beats frontier', 'humor improves accuracy', 'clinically safer', 'fine-tuned', or '50–70% funny'.

## Submission gate

Deadline 2026-11-03 00:30 UTC / Nov 2 16:30 PST includes upload and processing. Target video 115 seconds. Confirm public repository and exact commit access signed-out, setup/eval instructions, required fields, full roster and sponsor choices. Saving is not submitting. Final review/confirmation remains required before final submission; verify actual submitted status afterward. Stop development and evidence replacement at deadline; event-specific rules override generic platform update guidance.

Sources:
- https://hackersquad.io/events/fireworks-deploy-with-microsoft-nvidia/resources?tab=rules
- https://hackersquad.io/events/fireworks-deploy-with-microsoft-nvidia/resources?tab=submission
- https://github.com/zzfadi/product-factory/blob/3dbbdbb838a9e0e04338828b2e12576829c06c15/research/humor-classification/benchmark-contribution/dose-pilot/results.json
- https://github.com/kenn20/jokebench-rater-v2/blob/ee62cb1d3b7df4c4ab4311fc0b0e411af78e5311/data/fireworks-jokebench/README.md
