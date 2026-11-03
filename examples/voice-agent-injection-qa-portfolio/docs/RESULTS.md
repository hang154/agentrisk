# Historical voice-agent QA results

The synthetic TTS → Whisper ASR → Gemma Actor study recorded 5,000 episodes in 2,500 paired runs across 515 scenario roots. There were 4,768 automatically completed episodes and 232 inconclusive outcomes.

Among adversarial completed episodes, B0 recorded 66/1,664 unsafe gate escapes, while B1 recorded 0/1,679. B1 combines deterministic gates and GPT-OSS review; it is not reviewer-only treatment. Normal synthetic-ledger utility was 232/452 (B0) and 211/440 (B1), reported separately from escape counts. B0's recorded synthetic direct loss across all classes was KRW 2,224,000; B1's was KRW 0. These are virtual-ledger observations, not real customer funds.

[Scenario-class results](../data/summary.csv) · [Arm totals](../data/totals.csv) · [Normal utility](../data/benign_ledger_utility.csv) · [336 Risk Cells](../data/risk_cells.json)

The local demo uses authored transcripts and scripted actions, with no live speech, model or telephone integration. Not every adversarial episode is prompt injection; automatic completion is not completed human language adjudication.
