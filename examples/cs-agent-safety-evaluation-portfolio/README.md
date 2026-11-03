# Customer Support AI Agent QA — Task Success & Tool Safety

**Does your support agent resolve customer requests correctly *without* executing unauthorized refunds or account changes?**

This portfolio demonstrates how I build **repeatable agent evaluation harnesses** that inspect the tool boundary, not just LLM answers. It includes a runnable scripted demo, historical synthetic research aggregates and an example client handoff.

> **Research portfolio, not customer work.** The runnable eight-case demo is authored offline regression data; it does not re-run the original LLM experiments or access production APIs.

## In 60 seconds

| Real-world evaluation question | Demonstrated capability |
|---|---|
| Did the agent finish the intended task? | Independent expected outcomes and correct-completion counts |
| Could it perform a refund without transaction-level authorization? | Proposal → tool gate → virtual state change |
| Did a safety measure block legitimate work? | Normal-action completion and false-block counts |
| Was an outcome missing or ambiguous? | UNKNOWN is preserved, never reported as safe |

**Featured scripted scenario:** an over-refund slips through the pre-existing hard cap, but an authorization-bound amount check denies it before the virtual ledger changes. The baseline **already has authentication, account and hard-cap checks**.

## Run the demo (Python 3.10+, standard library only)

```bash
python3 evaluation.py demo
python3 evaluation.py verify
python3 -m unittest -v
python3 verify_release.py
```

[View committed output](reports/DEMO_OUTPUT.json) · [Client-style findings report](reports/SAMPLE_REPORT.md) · [60-second recording plan](docs/DEMO_STORYBOARD.md)

## Historical research, clearly separated

- **Legacy CS study:** 4,900 synthetic episodes comparing seven policies; not production client data.
- **Separate customer-case study:** 224 conditional Risk Cell aggregates. In a normal-case training comparison, Gemma state errors were **995 (B0) vs 362 (B3)** and Qwen **339 (B0) vs 90 (B3)**. These are historical study-specific comparisons, **not** the eight scripted demo cases, and should not be pooled with the legacy sample.
- **Controls:** B0 has existing hard gates; B3 combines task scope with a reviewer. Results do not isolate a reviewer-only causal effect.

[Method and denominators](docs/RESULTS.md) · [Research provenance](docs/PROVENANCE.md) · [Risk Cell projection](data/risk_cells.json)

## What a client receives

For one approved workflow, I can provide a 30–50-case evaluation plan, action-level expected-state checks, baseline-versus-guarded comparison, false-block and missing-outcome analysis, prioritized findings, runnable tests and a retest plan. The workflow, data use and any live integrations must be agreed before testing.

**[Service scope and intake](docs/SERVICE_BRIEF.md) · [Upwork-ready project description](docs/UPWORK_PORTFOLIO.md)**


## Public portfolio release

![Actual scripted offline evaluation report](media/demo-report.jpg)

[Open the rendered report](media/demo-report.html). This captured report uses the committed eight-case demo output; it is not a screenshot of new model inference.

This clean-history release contains QA code, authored fixtures, synthetic research aggregates, Risk Cells and client-delivery examples. No original model-response archive, customer data, deployment endpoints, weights or financial-pricing research is included.

[Reproduction and provenance](docs/PROVENANCE.md) · [Release checks](VALIDATION.json) · [Code license](LICENSE)
