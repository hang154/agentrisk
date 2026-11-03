# Upwork portfolio entry — Customer Support AI Agent QA & Tool Safety

**Portfolio title:** Customer Support AI Agent QA & Tool Safety

**Short description (copy into Upwork):**

I build offline, repeatable evaluations that show whether a support agent completes real work without over-refunding, duplicating transactions or crossing customer-account boundaries.

**Who this helps:** Teams automating refunds, account changes, and policy-driven customer support.

**Problem solved:** Which action can your agent take today: answer, issue a refund, or modify an account—and what approval or idempotency check should block it?

**Demonstrable evidence:** In one synthetic CS research cohort, Gemma state errors changed from 995 to 362 and Qwen state errors from 339 to 90 when comparing B0 and B3 controls. These are research results with study-specific denominators, not customer production outcomes.

**What I can deliver:** For one agreed CS workflow: document allowed tools and business rules; freeze 30–50 client-approved de-identified normal, edge and adversarial cases; build an independent state oracle; replay baseline and one guarded policy; report correct completions, unsafe state changes, false blocks and UNKNOWN; deliver regression tests and a retest plan.

**Example from the offline demo:** An over-refund is permitted by an existing baseline hard cap but rejected by a transaction-authorized amount check, before changing the virtual ledger.

**Evidence boundary:** The eight-case demo is an authored fixture, not a new LLM run. The 4,900 legacy episodes and 224 customer-case cells come from separate research populations.

## A first-client offer

- **Discovery:** agree on one workflow, allowed actions, independent success criteria and access permissions.
- **Fixed pilot:** up to 30–50 client-approved scenarios; a baseline/guarded comparison; output tables and a concise findings report.
- **Handoff:** scenario fixtures, deterministic regression checks, prioritized remediation proposals and one retest cycle.
- **Client responsibility:** provide or approve the test cases, synthetic or appropriately de-identified traces and an authorized isolated environment where required.
- **Not included:** formal penetration-testing attestation, live customer transactions, unsanctioned scans, model retraining, production deployment, or guaranteed incident reductions.
- **Integration:** live APIs, audio inference, complex DevOps or custom dashboards are separately scoped.

## Proposal opening — personalize before sending

Hi, I can help evaluate your AI agent against real task outcomes and tool-permission boundaries, not just its generated answers. My research portfolio includes customer support ai agent qa & tool safety, with a reproducible standard-library demo and explicitly bounded synthetic results. I would first agree on one workflow and 30–50 approved cases, then compare your current configuration to one guarded alternative and deliver action-level findings, regression tests and a retest plan. Could you share the agent's permitted actions and how your team currently decides whether the task was completed correctly?

## Suggested portfolio media

**Cover:** a real screenshot of the local evaluator showing a normal action, a blocked unsafe action, UNKNOWN and false-block counts (capture after running it; no invented metrics).

**60-second video:** record the steps in [the storyboard](DEMO_STORYBOARD.md). No video is included yet.

**Evidence:** [sample report](../reports/SAMPLE_REPORT.md) · [historical research](RESULTS.md) · [evaluation contract](EVALUATION_CONTRACT.md).

**Status:** independent personal research portfolio. Not a completed client engagement, production-security certification, or proof of reduced real-world incidents.
