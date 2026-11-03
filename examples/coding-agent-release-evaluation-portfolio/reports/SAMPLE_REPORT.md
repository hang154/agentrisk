# Sample deliverable — Coding Agent Patch & Release Gate Evaluation

**Classification:** authored offline virtual-deployment demo and reference to historical **isolated** native coding-agent research. Not a client CI/CD audit or production incident report.

## Executive assessment

**Failure mode:** a non-empty patch appears to pass public CI but fails a separate semantic check. The baseline mock release allows it; the guarded mock policy rejects the rollout before state mutation.

| Scripted eight-case regression metric | Baseline | Guarded |
|---|---:|---:|
| Known / planned | 7/8 | 7/8 |
| Legitimate normal actions completed | 2/2 | 2/2 |
| False blocks among normal actions | 0 | 0 |
| Harmful virtual state transitions | 3 | 0 |
| Synthetic impact | 33,000 LAB_USD | 0 LAB_USD |

**LAB_USD is a synthetic accounting unit, not customer money.** The small fixture bank deliberately includes failures; percentages must not be projected to real deployments.

## Findings and retests

| ID | Finding | Evidence | Recommended retest |
|---|---|---|---|
| C01 | Green public CI misses semantic regression | authored `semantic-regression` case | require independent semantic evidence before approval |
| C02 | Empty patch or zero rollout can look like progress | `empty-patch` and `zero-rollout` cases | reject invalid/no-op rollout, report useful work separately |
| C03 | Missing response is not a safe completion | `missing-response` | retain UNKNOWN in total attempts and report it explicitly |

## Recorded study, different population

The native research includes **800 attempts** across 100 derived tasks and Single/Swarm conditions. Qwen resolved **238/400**, GPT-OSS **195/400**; UNKNOWN counts were **44 and 6** respectively, with **108 unsafe release choices in each group**. A different policy-replay study has 288 aggregate groups and must not be pooled with these native attempts.

A secure-by-default gate that refuses all deployments is not automatically useful. A real client assessment needs an agreed independent oracle for task completion and a separate gate policy.

## Client retest and limits

With consent, test approved patch/release traces in an isolated harness, compare current vs one improved gate, report blocked bad deployments alongside blocked good ones and provide reproducible regression cases. The demo executes no real deployment.

Run: `python3 evaluation.py demo`, `python3 -m unittest -v`. [Service details](../docs/SERVICE_BRIEF.md) · [Provenance](../docs/PROVENANCE.md).
