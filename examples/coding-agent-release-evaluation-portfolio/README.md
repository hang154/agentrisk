# Coding Agent Evaluation — Patch Quality & Release Safety

**A coding agent can write a patch, pass CI, and still make a bad release decision.**

This portfolio evaluates **independent task resolution, unsafe rollout choices, semantic regression signals and tool permissions**. It includes a runnable offline release-gate demo and linked historical native coding-agent research.

> **Demo ≠ model run:** the eight local cases use authored patch/release signals and virtual deployment state. They do not run an LLM, execute untrusted code or deploy a service.

## Try a failed-semantic-check case

One scripted rollout has a non-empty patch and passing public CI but fails a semantic canary. The baseline accepts the virtual release; the guarded policy denies it due to missing semantic evidence.

```bash
python3 evaluation.py demo
python3 evaluation.py verify
python3 -m unittest -v
python3 verify_release.py
```

[Demo output](reports/DEMO_OUTPUT.json) · [Sample release findings](reports/SAMPLE_REPORT.md) · [60-second storyboard](docs/DEMO_STORYBOARD.md)

## Recorded native research — separately scoped

- **100 derived coding tasks × 2 models × Single/Swarm × 2 seeds = 800 native attempts**.
- Qwen resolved **238/400** with **44 UNKNOWN**; GPT-OSS resolved **195/400** with **6 UNKNOWN**. Both groups recorded **108 unsafe release decisions**.
- A different policy-replay population was summarized into **288 authority/control/economic cells**. This is **not** 288 more native model attempts and not observed customer production failure.
- A reviewer or hard gate that prevents every deployment is not inherently a good policy; legitimate work and false blocks must be measured.

[Study and denominators](docs/RESULTS.md) · [Provenance](docs/PROVENANCE.md) · [Risk Cell data](data/risk_cells.json)

## What a client receives

One approved repository/workflow evaluation with reproducible task and release checks, expected-state oracles, baseline/guarded comparisons, unsafe-release and false-block analysis, prioritized failures and a retest plan. Scoped local harness work is distinct from live production CI/CD integration.

**[Service proposal](docs/SERVICE_BRIEF.md) · [Upwork portfolio copy](docs/UPWORK_PORTFOLIO.md)**

All demonstration and research outcomes are synthetic or isolated. No production vulnerability, real financial loss or certified security assessment is claimed.


## Public portfolio release

![Actual scripted offline evaluation report](media/demo-report.jpg)

[Open the rendered report](media/demo-report.html). This captured report uses the committed eight-case demo output; it is not a screenshot of new model inference.

This clean-history release contains QA code, authored fixtures, synthetic research aggregates, Risk Cells and client-delivery examples. No original model-response archive, customer data, deployment endpoints, weights or financial-pricing research is included.

[Reproduction and provenance](docs/PROVENANCE.md) · [Release checks](VALIDATION.json) · [Code license](LICENSE)
