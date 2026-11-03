# JokeBench Rater

## Why This Project Exists

Language models can produce a joke, but “a joke” is not a useful quality bar. They often reuse familiar material, repeat the same premise across a batch, or fall into a reliable but stale structure such as “my therapist said X, so I did Y.” A benchmark needs to measure whether a prompt produces jokes that people actually find funny **and** whether it produces enough variety to remain useful.

JokeBench Rater is a small human-evaluation loop for that question. It generates comparable joke batches from several models, asks a human to rate each joke, and exports the evidence for later analysis.

## What This Project Does

1. Generates one-line jokes from multiple models through OpenRouter.
2. Compares a **harness** prompt against a **no-harness** prompt.
3. Shows only generated jokes in a local browser rater.
4. Captures human `funny` / `not funny` feedback.
5. Exports the reviewed dataset as JSON or CSV.
6. Detects and penalizes repeated jokes, repeated themes, and banned stale joke structures.

Current experiment: **V3 Diversity**. The rater serves 60 generated jokes and tests whether diversity-first prompting reduces repeated premises and structures.

## The Question V3 Answers

> Does assigning every joke a unique premise, while explicitly banning stale topics and structures, create a more varied set of jokes than a generic “make a joke” request?

The outcome is not decided by the prompt alone. A human reviewer still decides whether each joke is funny. Automatic penalties only record clear diversity failures, such as a repeated joke or a prohibited repeated structure.

## What V3 Tests

| Factor | Harness | No harness |
|---|---|---|
| Models | GLM 5.3 Flash, Nemotron 3.5 Lightning, DeepSeek V4.1 Flash | Same three models |
| Samples | 10 jokes per model | 10 jokes per model |
| Prompting | Human-rated examples supplied as context | Direct diversity-first request |
| Total | 30 | 30 |

V3 assigns every generated joke one distinct premise. It explicitly bans exhausted themes—therapy, calendars, houseplants, GPS, Wi-Fi, phones, and treadmills—and the repeated construction `X said/told/asked … so I did`.

Outputs violating a diversity rule are automatically marked `funny: false`, `complete: true`, and receive a `diversity_penalty` record. The current V3 dataset contains 60 unique scheduled themes and three automatically penalized violations.

## Quick Start

```bash
npm run serve
```

Open http://localhost:4173.

The app stores ratings only in browser `localStorage`. Use **Export JSON** or **Export CSV** after rating one or more jokes to download the dataset with feedback.

Keyboard shortcuts:

- `F` — funny
- `N` — not funny

## Validation

```bash
npm test
```

This verifies V3 dataset invariants and JavaScript syntax. V3 checks include:

- exactly 60 generated records and no human test records;
- 60 unique presentation IDs;
- 60 unique assigned themes;
- all diversity penalties are pre-labeled not funny;
- all non-penalized generated records remain unrated.

## Generate a New Dataset

Requirements: Node.js 18+ and an OpenRouter API key. Keep secrets in environment variables; never commit them.

```bash
export OPENROUTER_API_KEY='...'
export HUMAN_HARNESS_PATH='/path/to/human-harness-examples.json'
npm run generate:v3
```

`HUMAN_HARNESS_PATH` must reference the 20-item human-rating JSON used only for the harness context. Human examples are not included in the V3 rater dataset.

### Generation Scripts

- `generate-v2.mjs` — V2 originality experiment; detects textual near-repeats.
- `generate-v3.mjs` — current diversity experiment; assigns distinct themes and penalizes banned/repeated structures.

### Raw OpenRouter cURL Requests

Model-specific one-shot scripts are available for the V2 baseline:

```bash
scripts/generate-glm-v2.sh
scripts/generate-nemotron-v2.sh
scripts/generate-deepseek-v2.sh
```

Each requires `OPENROUTER_API_KEY` and writes only the model response to stdout.

## Repository Layout

```text
app.js                                         Static rater behavior and JSON/CSV export
index.html                                     Accessible rater UI
styles.css                                     Token-driven responsive styles
DESIGN.md                                      UI design system
generate-v2.mjs                                V2 originality experiment generator
generate-v3.mjs                                V3 diversity experiment generator
jokebench-openrouter-generated-60-v3-diversity.json  Current V3 rater dataset
tests/validate-dataset.sh                      V3 dataset invariant test
scripts/                                       Raw OpenRouter cURL examples
data/fireworks-jokebench/                      Separate Fireworks archive and human-evaluation material
```

## Dataset Fields

Each V3 item includes:

- `generation_model` and `generation_condition` for experiment provenance;
- `assigned_theme` for the diversity schedule;
- `response` for the generated one-liner;
- `funny` and `rated_at` for user feedback;
- `diversity_penalty` when automatic policy enforcement fired.

## Related Archive

The [Fireworks JokeBench archive](data/fireworks-jokebench/README.md) contains separate historical datasets, prompts, human rating sessions, and comparison charts. It is not part of the current V3 rater sample.
