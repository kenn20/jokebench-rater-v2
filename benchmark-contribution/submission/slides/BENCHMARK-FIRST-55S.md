# Benchmark narration — first 55 seconds

Ready-to-record draft; coordinate with three-slide deck. User handles app/second minute independently. All results below are audited recorded pilot values, not new execution. Final model identities unresolved: say requested aliases.

## Slide 1 · 0–18 seconds · Question and design
“Can we add humor without losing the task? We tested four humor instructions on the same questions and coding problems. This small pilot covers seventy tasks, two requested Claude aliases, and five hundred sixty responses. Humor was scored separately by a model judge.”

On-screen: 40 healthcare + 30 coding; 4 prompt levels; 2 requested aliases; 560 responses; one repeat. Prompt-only, not fine-tuning.

## Slide 2 · 18–40 seconds · Actual results
“With the strongest humor instruction, healthcare accuracy moved from seventy-five to seventy-two-point-five percent in one alias, and seventy-two-point-five to eighty-two-point-five in the other. That's mixed evidence, not proof humor improves accuracy. Coding was already at ceiling.”

On-screen: Haiku-requested 30/40 → 29/40; Sonnet-requested 29/40 → 33/40. Coding 30/30 in every arm. Show counts, not only percentages. Small exploratory paired result; Sonnet-alias p=.125.

## Slide 3 · 40–55 seconds · Honest takeaway
“Model-rated humor remained modest, below our fifty and seventy percent targets. This is a feasibility pilot, with unresolved model-identity receipts—not an established open-model win against a frontier baseline.”

On-screen: strongest model-rated funny >=3 rates 6.67–22.5%; not human clinical validation; public tasks; custom coding tests. Transition: separate simulated-patient demonstration, handled by user.

## Recorder note
Target 55 seconds at natural pace; trim pauses rather than caveats. Do not call 560 records 560 independent questions. Do not mix JokeBench human ratings into this chart. Use exact source commit 3dbbdbb838a9e0e04338828b2e12576829c06c15 and final audit at /workspace/shared/humor-results-audit/RESULTS-AUDIT.md. No automatic final submission.
