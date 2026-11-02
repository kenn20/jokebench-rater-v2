#!/usr/bin/env bash
set -euo pipefail

: "${OPENROUTER_API_KEY:?Set OPENROUTER_API_KEY before running this script}"

curl --fail-with-body --silent --show-error https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer ${OPENROUTER_API_KEY}" \
  -H 'Content-Type: application/json' \
  --data '{
    "model": "nvidia/nemotron-3.5-lightning",
    "messages": [{"role":"user","content":"Make exactly one original, self-contained, one-line joke. Originality is preferred. Return only the joke."}],
    "temperature": 1.05,
    "max_tokens": 512,
    "reasoning": {"effort":"none"}
  }' | jq -r '.choices[0].message.content'
