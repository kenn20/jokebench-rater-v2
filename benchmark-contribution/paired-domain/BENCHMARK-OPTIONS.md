# Known benchmark options — recommendation, not selection

Official sources inspected 2026-11-02. No corpus downloaded, copied, executed or uploaded. Actual benchmark/model/humor settings remain unset.

## Healthcare-domain recommendation: PubMedQA expert-labeled PQA-L

[Project](https://pubmedqa.github.io/) describes biomedical research questions answered yes/no/maybe from abstracts, with1,000 expert-labeled examples (distinct from unlabeled/artificially generated sets). [Author repository](https://github.com/pubmedqa/pubmedqa) provides split preprocessing and the PMID-to-label prediction format; [repository license](https://github.com/pubmedqa/pubmedqa/blob/master/LICENSE) is MIT. Preserve required notices and provenance; a repository license is not a blanket determination of rights in every underlying published abstract. Verify the chosen asset's notices before redistribution. Keep licensed task data custodian-local, not in this contribution.

**Proposed compact pilot:** preregister50 eligible items drawn by a fixed seed from the official heldout expert-labeled split, no outcome-based selection. Report label distribution; do not substitute generated labels. Use the same question/context and PMID in both conditions. Exclude answer-bearing conclusion/rationale fields from input under the benchmark's reasoning-required protocol. Verify this against the pinned preprocessing before running. Score answer labels with official accuracy and macro-F1, preserving invalid/missing predictions and coverage; the current scaffold implements exact-string accuracy only, so official macro-F1 parity still requires an adapter/test.

This is biomedical abstract comprehension, NOT patient care, diagnosis or clinical safety validation. No real patient records. Humor belongs in separate commentary, never a corrupted yes/no/maybe answer or mocking patient material. Report safety and usefulness separately. Fifty items are a pipeline pilot, not a leaderboard replication or evidence of clinical competence. Published data may occur in pretraining.

**Alternative requiring additional rights review:** MedQA. [Original author repository](https://github.com/jind11/MedQA) is the provenance source; [BigBio's card](https://huggingface.co/datasets/bigbio/med_qa/blob/main/README.md) currently marks license unknown. Do not infer that exam-question rights are settled by a code-repository license. Not recommended as the first immediate import.

## Programming recommendation: HumanEval, with HumanEval+ as robustness follow-on

[Official HumanEval repository](https://github.com/openai/human-eval) provides functional-correctness evaluation and explicitly warns that generated code needs a robust security sandbox. [License](https://github.com/openai/human-eval/blob/master/LICENSE) is MIT; retain notices. Recommend a preregistered32-task subset for the first paired pipeline pilot; later run the entire benchmark for a comparable result. Same tasks, one sample per arm for descriptive pass@1, same checkpoint/settings and frozen timeout policy. Do not report pass@k estimates unsupported by sample count. Failures/timeouts remain in the denominator.

Separate executable code from humor commentary using a fixed parser chosen before results. Do not execute model code in this ordinary workspace, privileged containers, or a network-enabled environment. An approved isolated sandbox with resource limits and the pinned official tests is a concrete prerequisite. The present exact-string scorer cannot measure code correctness; this contribution explicitly does not pretend it can.

[EvalPlus](https://github.com/evalplus/evalplus) adds stronger HumanEval+/MBPP+ tests and identifies an Apache-2.0 repository license. If selected, separately preserve base-dataset notices and exact test-suite version. Keep base and enhanced scores distinct; do not silently mix test suites across arms. Public tasks carry memorization risk; no claim of unseen capability.

## Optional third domain

[GSM8K official repository](https://github.com/openai/grade-school-math) is a possible arithmetic-reasoning follow-on, not selected. Review its license/notices and official numeric-answer parsing before importing. Do not use the synthetic2+2 software fixture as benchmark evidence. Prefer finishing healthcare/programming pipeline validity before expanding.

## Preregistered reporting and decision

Primary question per domain: does the frozen same-model humor intervention change task performance? Report paired score delta, wins/losses/ties, sample size, failures, coverage, latency and unknown costs. Independently demonstrate that humans actually found the humor-condition outputs funnier; an instruction to be funny does not establish that. Analyze all assigned items (intention-to-treat), not only outputs judged funny. Show paired human ratings and disagreements; do not pool unequal-rating cohorts for claimed lift. Any within-output funniness/task correlation is exploratory, not proof humor caused performance changes.

A32/50 pilot is too small for broad superiority claims; preregister uncertainty estimation and repeat policy before a confirmatory run. No pooled healthcare/programming score unless weighting is specified in advance. Frontier comparison is optional secondary context and cannot block the primary pair or alter its denominator.
