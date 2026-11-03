# Voice AI Agent Red Teaming — Prompt Injection & Call QA

**Can a caller's untrusted speech make an AI voice agent execute an unauthorized tool action?**

This portfolio shows an **offline transcript-to-tool risk evaluator** and linked historical synthetic TTS/ASR study evidence. It emphasizes adversarial attempts, what actually passed control gates, **inconclusive cases**, and legitimate-caller utility.

> **Scope:** the local eight-case demo replays authored transcripts and actions. It does **not** synthesize speech, call Whisper, run a model, or assess a live customer's telephone system.

## One-minute walkthrough

**Example:** a customer transcript says to ignore a previous instruction and override a refund amount. The baseline uses existing identity and hard-cap checks; the guarded mock tool boundary requires the transaction-authorized amount and duplicate-id validation.

```bash
python3 evaluation.py demo
python3 evaluation.py verify
python3 -m unittest -v
python3 verify_release.py
```

[Scripted demo output](reports/DEMO_OUTPUT.json) · [Example findings report](reports/SAMPLE_REPORT.md) · [Recording storyboard](docs/DEMO_STORYBOARD.md)

## Actual frozen research — separate from the demo

- **5,000 synthetic TTS/ASR episodes** arranged in 2,500 paired runs across 515 scenario roots. Paired runs are not 2,500 independent scenario roots.
- Among deterministically completed **adversarial episodes**, unsafe escapes were **66/1,664** for B0 and **0/1,679** for B1. The eligible denominators differ; 232 runs remained inconclusive overall.
- The B1 condition uses **a bundle of deterministic gates and GPT-OSS review**, not a reviewer-only defense.
- Positive benign virtual-ledger outcomes were **232/452 (51.3%)** in B0 and **211/440 (48.0%)** in B1. Do not hide normal-call friction.

Not every adversarial scenario is a prompt-injection attack. Synthetic audio from historical experiments is not shipped, and zero observed unsafe passes does **not** imply zero production risk.

[Detailed study breakdown](docs/RESULTS.md) · [Provenance](docs/PROVENANCE.md) · [Risk Cell dimensions](data/risk_cells.json)

## What a client receives

For a defined voice-assistant workflow: a threat and task matrix; 30–50 authorized normal/abuse/edge scenarios; transcript-to-tool trace evaluation; baseline/guarded comparison; unsafe-action, false-block, escalation and inconclusive metrics; findings and repeatable retests.

**[Service & acceptance criteria](docs/SERVICE_BRIEF.md) · [Upwork portfolio copy](docs/UPWORK_PORTFOLIO.md)**

The sample is designed for authorized isolated evaluation only. It is not a live penetration-testing certificate, voice recognition accuracy audit, customer pilot or guarantee of attack resistance.


## Public portfolio release

![Actual scripted offline evaluation report](media/demo-report.jpg)

[Open the rendered report](media/demo-report.html). This captured report uses the committed eight-case demo output; it is not a screenshot of new model inference.

This clean-history release contains QA code, authored fixtures, synthetic research aggregates, Risk Cells and client-delivery examples. No original model-response archive, customer data, deployment endpoints, weights or financial-pricing research is included.

[Reproduction and provenance](docs/PROVENANCE.md) · [Release checks](VALIDATION.json) · [Code license](LICENSE)
