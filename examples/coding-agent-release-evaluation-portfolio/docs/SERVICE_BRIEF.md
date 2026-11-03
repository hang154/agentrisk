# Client-facing service brief — Coding Agent QA & Release Decision Evaluation

**Target buyer:** teams using coding agents for patches, PRs, test execution or deployment preparation.

**Problem:** A patch may satisfy public unit tests yet change business semantics or be released without the required evidence. Some protections simply block all releases, so both safety and developer productivity matter.

## Initial fixed-scope evaluation

1. Freeze one repository/workflow and define what constitutes a resolved task independently of the agent's self-report.
2. Select 30–50 approved patch/PR or release-decision cases, with agreed oracle and release permission matrix.
3. Evaluate patch presence, test evidence, semantic checks, proposed rollout percentage and authorization.
4. Compare baseline and a selected guarded release decision; retain false blocks and UNKNOWN.
5. Deliver machine-readable run summaries, reproducible fixtures, a ranked finding register, remediation guidance and one retest.

**Customer input:** permitted repository scope, prepared tasks, test oracles, approved isolated environment, CI artifacts and authorization boundary. No production credential sharing at discovery.

**Out of scope until separately contracted:** unrestricted penetration testing, arbitrary remote command execution on production, production deploys, arbitrary agent modification, model post-training or unbounded acceptance testing.

## Acceptance

Success and release-safety are separate metrics. A tool-call suggestion does not prove that code was deployed. Missing runs are not counted as task success or safety. Retests use a frozen case bank and documented environment versions.

## Proposal sample

I can help audit your coding-agent workflow beyond whether its generated patch looks plausible or public CI passes. I'd start with one codebase and a fixed set of 30–50 approved tasks/release decisions, define an independent acceptance oracle, then compare the current gate with a stronger candidate while tracking resolved work, unsafe release choices and false blocks. The portfolio demonstrates this approach with an offline mock and separate native research evidence; it is not a production deployment claim. What harness and test oracle do you use for agent-generated changes?

[Upwork description](UPWORK_PORTFOLIO.md) · [Sample report](../reports/SAMPLE_REPORT.md) · [Research scope](RESULTS.md)
