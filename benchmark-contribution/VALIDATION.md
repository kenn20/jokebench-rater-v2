# Local validation receipt

2026-11-02 UTC. Base: team main de2febd0b6aedbac31a5b7436fe306c0fa18419f, exact tree 0bc52eb9dd19a0242332987d01f7fbb3021494a2 reconstructed before additive changes.

Passed:
- `npm test`: existing 60-row dataset invariant and syntax checks for app.js / generate-v2.mjs.
- `python3 -m unittest discover -s benchmark-contribution -p test_team_export_audit.py -v`: 8 tests.
- `(cd benchmark-contribution/humor-classification && python3 -m unittest -v test_classify.py)`: 13 tests.
- `(cd benchmark-contribution/paired-domain && python3 -m unittest -v)`: 19 tests.
- Python compile, contribution manifest hashes, staged whitespace/diff and credential-pattern review.

40 new offline tests total. All use software fixtures, not actual human ratings or model predictions. Audit of existing checked-in data: 60 items, 0 explicit timestamped votes, 2 automatic originality penalties kept separate. No generation/API/network script was run. Browser rendering and human interpretation were not tested. Model IDs, common benchmark and intervention remain unselected. Remote CI has not run for this local contribution.

Before remote delivery, upstream advanced to3918cafabde557a07c007952038ba458ad89e614. Refreshed its33 changed text files locally and reran npm test plus `python3 scripts/validate-fireworks-archive.py` (8datasets/4sessions: PASS). Four unchanged upstream chart files were preserved by the remote base tree, not rendered or revalidated. No contribution paths overlap upstream changes. All40 contribution tests rerun after refresh: PASS.

Factory mirror validation, 2026-11-02: active SPI 19, factory 4, governance 8, original classification 13, mirrored classification 13, audit 8, paired-domain 19 = 84 offline tests passed. build_spi, factory check, govern, income_check and secret scan passed. First source-manifest directory entry failed baseline check; corrected to exact file paths and reran all gates successfully. Generated dist outputs excluded. No remote CI or real model run claimed.
