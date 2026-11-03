# Humor × Performance — Pilot Observatory

Repo-local static dashboard for the consolidated benchmark submission. Open `index.html` in a desktop browser; no build, install, network, API key, model call, server or daemon is required. Copy the entire directory together. This package is suitable for `benchmark-contribution/submission/dashboard/`; the parent task owns repository integration and PR work. Nothing here publishes a website.

## Evidence and scope

The default view is requested **Sonnet alias / PubMedQA**, with selectors for Haiku and HumanEval. All 16 rows are from an independent artifact audit of source commit `3dbbdbb838a9e0e04338828b2e12576829c06c15` in `zzfadi/product-factory`, path `research/humor-classification/benchmark-contribution/dose-pilot`.

- 560 unique recorded task outputs and 560 recorded model judgments cover 70 distinct tasks, 2 requested model aliases, 2 domains and 4 humor instructions.
- Healthcare exact-match answers were independently rescored. Programming pass flags were aggregated **without re-executing generated code**.
- Humor is model-judged, not human rated. `funny_ge3_rate` is the count rated at least 3/5 divided by the judged arm count. All arms have complete judgment coverage.
- 50% / 70% are desired funny-rate reference targets, not implemented or achieved doses. The maximum observed rate is 22.5%.
- Model names are **requested CLI aliases**, not isolated checkpoint attribution: 278/280 Sonnet-alias task receipts and all 560 judge receipts list both Haiku and Sonnet usage.
- Counts and ratios use exact audit rows, not rounded source presentation. Decimal displays are rounded to at most two percentage decimals. Mean humor displays three decimals.
- Paired W/L/T compares correctness on identical items. The p-values are exploratory, two-sided exact sign tests, with no multiple-testing adjustment. No causal, universal uplift, non-inferiority, fine-tuning, clinical or safety claim is made.
- 56 raw output formatting exceptions parse after the source's documented fence/brace recovery; these are not 56 missing outputs.
- The five-round Slack image is intentionally not embedded or linked; it is separate private/source-reported evidence and must not be conflated with this automated pilot.

## Files

- `index.html`, `styles.css`, `app.js`: UI; no external dependencies.
- `data.js`: offline runtime mirror of `data/dashboard.json` (no fetch/CORS requirement).
- `data/dashboard.json`, `data/audit-results.json`: identical audited exact metrics and scope metadata.
- `data/metrics.csv`: all 16 arms for spreadsheet use.
- `data/RESULTS-AUDIT.md`: independent audit narrative.
- `test.cjs`: dependency-free Node data/static/DOM-contract checks.
- `qa.cjs`: optional Playwright browser smoke test, using a locally installed Chromium; not a runtime dependency.

## Validation performed

`node --check app.js`, `node --check data.js`, and `node test.cjs` pass. Tests verify row arithmetic and counts, the source pin, audit equality, all local links, no external runtime assets, repeated model/domain switching, chart generation and theme switching with blocked local storage.

Actual browser screenshots and layout checks could not run in this cloud executor because browser launch was restricted. No screenshot or browser pass is claimed. Before a live presentation, a supported executor should run `node qa.cjs` (Playwright available) or open `index.html`, inspect 1440px and 390px widths, switch every filter, expand the exact table, toggle themes and download the data. The template includes responsive breakpoints, semantic headings/fieldset buttons, chart labels, keyboard focus, reduced-motion support and a noscript data fallback; visual accessibility is not independently certified.

## Refreshing the frozen data

Only replace the two JSON snapshots from a finalized audit. Regenerate `data.js` as `window.DASHBOARD_DATA = <JSON>;` (escape closing-tag sequences), and regenerate the CSV with the same row keys. Run the tests and update source provenance and narrative together; do not insert estimates or live model calls. The current headline is intentionally specific to this frozen pilot and must be reviewed if data changes.
