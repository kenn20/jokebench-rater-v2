# JokeBench Rater V2

Static browser rater for 60 generated jokes from GLM 5.3 Flash, Nemotron 3.5 Lightning, and DeepSeek V4.1 Flash. It records funny/not-funny feedback in browser storage and exports JSON or CSV.

## Run

```bash
npm run serve
```

Open http://localhost:4173.

## Test

```bash
npm test
```

## Regenerate V2

Set an OpenRouter key only in your shell; never commit it:

```bash
export OPENROUTER_API_KEY='...'
export HUMAN_HARNESS_PATH='/path/to/human-harness-examples.json'
npm run generate:v2
```

Generation requires exactly one original self-contained one-line joke. The harness condition uses the 20 human-rated examples only as generation context; the exported rater dataset contains only 60 generated test cases.

`generate-v2.mjs` automatically labels exact/near repeats `funny: false` using Jaccard similarity ≥0.50 or a shared eight-word phrase.

## Raw OpenRouter cURL examples

Each script requires `OPENROUTER_API_KEY`; scripts do not store credentials.

```bash
scripts/generate-glm-v2.sh
scripts/generate-nemotron-v2.sh
scripts/generate-deepseek-v2.sh
```

## Fireworks datasets and human evaluations

See [the Fireworks JokeBench archive](data/fireworks-jokebench/README.md) for eight 20-item datasets, four verified human rating sessions, exact generation prompts, and comparison charts. These remain separate from the existing OpenRouter rater dataset.
