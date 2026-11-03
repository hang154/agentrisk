# Upwork portfolio entry — Coding Agent QA | Patch, Release & Permission Gates

**Portfolio title:** Coding Agent QA | Patch, Release & Permission Gates

**Short description (copy into Upwork):**

I evaluate coding agents beyond green tests: independent task resolution, bad patch proposals, unsafe release choices and tool-permission boundaries.

**Who this helps:** Teams using autonomous code agents to propose patches, run tests or initiate deployments.

**Problem solved:** If an agent's patch passes public CI but fails a semantic canary, can the release action still cross the gate?

**Demonstrable evidence:** 800 native coding-agent attempts across 100 derived tasks, with Single/Swarm conditions and two seeds. Qwen resolved 238/400 recorded attempts and GPT-OSS 195/400, with 44 and 6 UNKNOWN respectively. Both model groups recorded 108 unsafe release choices. The separate 288 authority/control scenario groups are not additional native coding attempts.

**What I can deliver:** For an agreed repository/harness: define independent pass/fail oracles and release criteria; freeze 30–50 authorized patch or release-decision cases; test empty patches, green CI with semantic regression, unsafe rollout requests, approval gates and aborts; report resolved work, unsafe release choices, false blocks and unknowns; deliver deterministic regression tests and retest evidence.

**Example from the offline demo:** A non-empty patch passes public CI but fails a semantic canary. A baseline accepts the proposed virtual rollout; the guarded release decision rejects it.

**Evidence boundary:** The eight-case runnable demo uses authored release decisions and mock deployment state. Native research runs are distinct from policy replay simulations. No live production deployments or customer incidents are claimed.

## A first-client offer

- **Discovery:** agree on one workflow, allowed actions, independent success criteria and access permissions.
- **Fixed pilot:** up to 30–50 client-approved scenarios; a baseline/guarded comparison; output tables and a concise findings report.
- **Handoff:** scenario fixtures, deterministic regression checks, prioritized remediation proposals and one retest cycle.
- **Client responsibility:** provide or approve the test cases, synthetic or appropriately de-identified traces and an authorized isolated environment where required.
- **Not included:** formal penetration-testing attestation, live customer transactions, unsanctioned scans, model retraining, production deployment, or guaranteed incident reductions.
- **Integration:** live APIs, audio inference, complex DevOps or custom dashboards are separately scoped.

## Proposal opening — personalize before sending

Hi, I can help evaluate your AI agent against real task outcomes and tool-permission boundaries, not just its generated answers. My research portfolio includes coding agent qa | patch, release & permission gates, with a reproducible standard-library demo and explicitly bounded synthetic results. I would first agree on one workflow and 30–50 approved cases, then compare your current configuration to one guarded alternative and deliver action-level findings, regression tests and a retest plan. Could you share the agent's permitted actions and how your team currently decides whether the task was completed correctly?

## Suggested portfolio media

**Cover:** a real screenshot of the local evaluator showing a normal action, a blocked unsafe action, UNKNOWN and false-block counts (capture after running it; no invented metrics).

**60-second video:** record the steps in [the storyboard](DEMO_STORYBOARD.md). No video is included yet.

**Evidence:** [sample report](../reports/SAMPLE_REPORT.md) · [historical research](RESULTS.md) · [evaluation contract](EVALUATION_CONTRACT.md).

**Status:** independent personal research portfolio. Not a completed client engagement, production-security certification, or proof of reduced real-world incidents.
