# Humor Lab: first-minute benchmark deck

Three 16:9 slides for the benchmark portion of the hackathon video. The app demonstration belongs to the separate second minute.

- `humor-lab-benchmark.pptx`: editable PowerPoint, including a native grouped-column chart with an embedded workbook and speaker notes.
- `humor-lab-benchmark.pdf`: recording/presentation copy exported from the finalized PPTX using LibreOffice.
- `BENCHMARK-FIRST-55S.md`: narration and timing guide, approximately 55 seconds.
- `previews/`: all three PDF pages rendered at 96 DPI.
- `audited-summary.json`: independently reconciled summary of the recorded pilot artifacts.

## Source and interpretation

Exact source commit: `3dbbdbb838a9e0e04338828b2e12576829c06c15`.

[Recorded pilot results](https://github.com/zzfadi/product-factory/blob/3dbbdbb838a9e0e04338828b2e12576829c06c15/research/humor-classification/benchmark-contribution/dose-pilot/results.json)

560 recorded responses cover 70 distinct public tasks, four prompt levels, two requested Claude aliases, and one repeat. This is a prompt-only pilot. The final response model cannot be independently established from mixed model-usage receipts, so the deck consistently labels requested aliases.

Healthcare values reconcile with stored answer keys. Coding values aggregate stored pass flags and were not independently rerun. Humor is a model-judge rating of at least 3/5, not a human panel. The 50% and 70% humor targets were not reached. Sonnet-requested healthcare's +10 percentage points are exploratory, with four wins, no losses and 36 ties over 40 pairs; exact two-sided paired sign test p=.125. No causal improvement, clinical validation, fine-tuning or open-model/frontier superiority is claimed. The separate five-round team joke data is not combined with this pilot.

## Verification

All three final PDF pages and Artifact Tool PNG previews were visually inspected. No unintended overlap or clipping was found. Structural package, slide-count, geometry, fonts, native chart and workbook-cache validation passed. PowerPoint itself was not opened, so native PowerPoint rendering is unverified. The PDF is the visually checked recording fallback.

The native Artifact Tool PDF exporter lacked its Helvetica module; the successful PDF export uses LibreOffice instead. No new model calls, external hosting or generated-code execution occurred.
