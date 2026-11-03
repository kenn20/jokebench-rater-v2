# Independent annotation instructions — original40 v1
Purpose: subjective funniness classification for general adult English-speaking readers in a casual, non-clinical context. Not therapy, clinical care, marketing effectiveness or a test of whether text resembles a joke.

You receive item_id and full text only. Do not look up sources, use LLMs for votes, read model outputs, or consult other raters before submitting. Do not infer a label from paired formatting or author intent. Every label begins unknown. Evaluate each item independently; a joke attempt may be unfunny and ordinary wording may amuse you.

Enter your stable pseudonymous rater_id (no email/phone needed), then:
- funny: you personally find this text at least mildly amusing in the stated context.
- not_funny: you do not find it amusing, even if you recognize the intended joke.
- unsure: you cannot decide or don't understand context/wordplay well enough. Never guess to fill a quota.
Separately safety_flag: none / concern / decline. “Concern” does not automatically mean not_funny. “Decline” means you prefer not to assess; set label=unsure and optional comment if comfortable. No need to quote objectionable text in comments.

At least3independent raters per item; keep every vote. A funny/not_funny consensus requires strictly more than half of all votes and>=3unique raters. Otherwise label remains unresolved; do not drop that item invisibly. Rater disagreement is a result, not a nuisance to erase. Optional adjudication must be documented separately after original votes are preserved.

The all40 CSV is custodian/annotator material: NO TUNING, no posting to team channels, no model upload. Developer export contains dev only. Keep all held-out texts, human ratings and author-intent notes away from prompt designers until model/harness/settings freeze. Do not claim balance, representativeness,100-case completion or model performance from this candidate pool. No human ratings have yet been obtained.
