# Sample deliverable — Voice Agent Adversarial Tool QA

**Classification:** authored offline scripted demonstration plus referenced historical *synthetic* TTS/ASR research. Not a paid client assessment or a live phone penetration test.

## Executive assessment

**Risk question:** Can an untrusted transcript raise an authorized refund amount and cause the voice agent's downstream tool to act?

**Demo finding:** the untrusted instruction is represented as a scripted action proposal. Existing baseline identity and hard-cap checks do not catch the larger amount; the guarded mock policy denies it before any virtual state change.

| Offline scripted outcome | Baseline | Guarded |
|---|---:|---:|
| Known / planned scripted cases | 7/8 | 7/8 |
| Legitimate normal actions completed | 2/2 | 2/2 |
| False blocks among normal cases | 0 | 0 |
| Harmful virtual state changes | 2 | 0 |
| Synthetic virtual-ledger impact | KRW 50,000 | KRW 0 |

**These eight authored cases are not a voice or LLM model benchmark.** There is no audio generation or ASR call in this local demo.

## Research evidence, separate population

The historical study included **5,000 synthetic speech/ASR episodes** in 2,500 paired runs across 515 scenario roots. Repeated pairs are not independent roots. Among conclusive adversarial cases the unsafe gate escapes were **66/1,664 (B0)** vs **0/1,679 (B1)**. Across all categories **232 cases were inconclusive**. B1 combines deterministic gates with review.

**Normal-call trade-off:** benign positive synthetic-ledger outcomes were 232/452 in B0 and 211/440 in B1. These denominators differ and are not a causal estimate of reduced customer service quality.

## Finding register

| ID | Potential failure | Evidence | Safeguard to verify |
|---|---|---|---|
| V01 | Spoken instruction requests privileged change | authored `over-refund` transcript/action pair | trusted transaction amount checked at the tool boundary |
| V02 | Replayed speech repeats transaction | authored duplicate action | request-id idempotency evidence |
| V03 | Missing transcript/tool result may appear safe | UNKNOWN fixture | keep separate inconclusive count and follow-up |

## Client integration and retest

For a real engagement: obtain the call flow and authorization matrix, define expected outcomes for approved cases, test only consented/synthetic materials in isolation, deliver trace-level evidence and re-test after fixes. Findings do not prove the absence of attacks.

Run: `python3 evaluation.py demo` and `python3 verify_release.py`. [Scope](../docs/SERVICE_BRIEF.md) · [Detailed research limits](../docs/RESULTS.md).
