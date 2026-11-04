# Historical Voice disagreement audit

The frozen archive was read without changing the original labels or loss results.
All eight archive-part SHA-256 hashes and the concatenated archive hash matched;
all **2,114 reconstructed wire-input hashes** matched the original protocol lock.
The original source-packet hashes describe the preblinding packets, so they must
not be confused with transformed blind-packet byte hashes.

| Same frozen selected subset | Count |
|---|---:|
| Mechanical unsafe execution | 119 |
| Qwen unsafe execution observed | 2 |
| Mechanical unsafe / Qwen not observed | 117 |
| Neither flagged | 1,995 |

A new transcript-only screen flags 61 disagreement packets with a later confirmed
amount different from the recorded transaction, 40 with no explicit `I confirm`
amount found by the screen, 11 outside the visible refund window and one above
its visible amount limit. Categories overlap. The phrase screen can miss valid
confirmations and does not resolve currency/exception/context ambiguity. These
are **review triage flags, not new gold labels or an estimated monitor miss rate**.

A blinded review package contains all 117 disagreements and 40 cases drawn
randomly within the original enriched 2,114-case subset: 156 unique packets after
one overlap. Reviewer 1/2 forms are blank. The unblinding map is separate. No human
review or third-party adjudication has occurred. Random-within-selected-corpus
is not a random sample of the original 5,000 episodes.

The current experiment therefore compares monitor information conditions on
new, timestamped execution receipts, rather than treating this historical
comparison as proof of the language model's error rate. The new policy oracle,
monitor target and post-action timing are explicitly aligned.

Machine-readable audit: `artifacts/control_study_202611/LEGACY_DISAGREEMENT_AUDIT.json`.
Historical source: `research/archive/results/voice_redteam5000_20261009/ai_third_party_qwen_v11/FINAL_REPORT_KO.md`.
