#!/usr/bin/env bash
set -euo pipefail

dataset="jokebench-openrouter-generated-60-v3-diversity.json"

jq -e '
  . as $dataset
  | ([.ratings[] | select(.generation_model != null)] | length) as $generated
  | ([.ratings[] | select(.generation_model == null)] | length) as $human
  | ([.ratings[] | select(.diversity_penalty != null)] | all(.[]; .funny == false and .complete == true)) as $penalties
  | ([.ratings[] | select(.generation_model != null and .diversity_penalty == null)] | all(.[]; .funny == null and .complete == false)) as $unrated
  | if .schema_version == 7
      and .dataset_version == "jokebench-openrouter-generated-60-v3-diversity"
      and ($dataset.ratings | length) == 60
      and $generated == 60
      and $human == 0
      and ($dataset.presentation_order | length) == 60
      and ($dataset.presentation_order | unique | length) == 60
      and (($dataset.presentation_order | sort) == ($dataset.ratings | map(.item_id) | sort))
      and ([.ratings[].assigned_theme] | unique | length) == 60
      and $penalties
      and $unrated
    then "dataset validation passed"
    else error("generated-only V3 dataset invariant failed") end
' "$dataset"
