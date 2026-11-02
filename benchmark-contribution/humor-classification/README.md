# Development-only humor classification tools

20 original synthetic development candidates, empty human-vote templates and an offline classification scorer. These are not an established benchmark or a funny/not-funny gold set. No human labels or model runs are included. The source authoring process paired thematic contrasts; this is a small convenience sample, not representative humor.

From this folder run `python3 -m unittest -v test_classify.py` and `python3 classify.py score --items dev-items.json --annotations annotation-template.json --runs empty-runs.json`. The latter must return not_run and null metrics.

Use ANNOTATOR-RUBRIC.md before obtaining independent votes. Intended humor is not a label. Keep any heldout pool outside the development tree; no heldout texts, private notes or account details are included. This classification component measures predictions against a human panel; it does not replace blind human evaluation of generated jokes, or deterministic common-benchmark scoring. Never convert originality penalties into human humor votes. No API calls or dependencies beyond Python's standard library.
