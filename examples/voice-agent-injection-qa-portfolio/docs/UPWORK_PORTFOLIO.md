# Upwork portfolio entry — Voice AI Agent Red Teaming & Tool-Action QA

**Portfolio title:** Voice AI Agent Red Teaming & Tool-Action QA

**Short description (copy into Upwork):**

I test whether a voice assistant can resist adversarial instructions and still complete legitimate customer requests, with a focus on the boundary between transcripts and tools.

**Who this helps:** Teams building voice assistants, reservation agents and phone-based customer support.

**Problem solved:** Can caller speech change a payment amount, account owner or workflow instructions without the trusted system authorizing it?

**Demonstrable evidence:** 5,000 synthetic TTS/ASR study episodes in 2,500 paired runs across 515 scenario roots, not 2,500 independent scenarios. Among conclusive adversarial episodes, unsafe escapes were 66/1,664 under B0 versus 0/1,679 under B1. There were 232 inconclusive runs across the study. The strengthened configuration combined deterministic gates with a reviewer; it also changed benign positive-ledger outcomes (232/452 vs 211/440).

**What I can deliver:** For one voice-support workflow: define legitimate intents and allowed tool actions; freeze 30–50 authorized test transcripts or consented recordings; evaluate scripted/adversarial cases, identity checks, tool permissions, handoffs and expected virtual state; show baseline vs guarded outcome, missed/uncertain cases and normal-call impact; provide a regression suite and report.

**Example from the offline demo:** An untrusted transcript asks to override a refund amount; the guarded policy validates the amount against trusted transaction state before the mock tool action.

**Evidence boundary:** The runnable portfolio demo replays authored transcripts and scripted tool actions; it does not synthesize audio, call Whisper or run an LLM. Not all adversarial episodes are prompt injection, and zero observed passes is not a guarantee of zero real-world failures.

## A first-client offer

- **Discovery:** agree on one workflow, allowed actions, independent success criteria and access permissions.
- **Fixed pilot:** up to 30–50 client-approved scenarios; a baseline/guarded comparison; output tables and a concise findings report.
- **Handoff:** scenario fixtures, deterministic regression checks, prioritized remediation proposals and one retest cycle.
- **Client responsibility:** provide or approve the test cases, synthetic or appropriately de-identified traces and an authorized isolated environment where required.
- **Not included:** formal penetration-testing attestation, live customer transactions, unsanctioned scans, model retraining, production deployment, or guaranteed incident reductions.
- **Integration:** live APIs, audio inference, complex DevOps or custom dashboards are separately scoped.

## Proposal opening — personalize before sending

Hi, I can help evaluate your AI agent against real task outcomes and tool-permission boundaries, not just its generated answers. My research portfolio includes voice ai agent red teaming & tool-action qa, with a reproducible standard-library demo and explicitly bounded synthetic results. I would first agree on one workflow and 30–50 approved cases, then compare your current configuration to one guarded alternative and deliver action-level findings, regression tests and a retest plan. Could you share the agent's permitted actions and how your team currently decides whether the task was completed correctly?

## Suggested portfolio media

**Cover:** a real screenshot of the local evaluator showing a normal action, a blocked unsafe action, UNKNOWN and false-block counts (capture after running it; no invented metrics).

**60-second video:** record the steps in [the storyboard](DEMO_STORYBOARD.md). No video is included yet.

**Evidence:** [sample report](../reports/SAMPLE_REPORT.md) · [historical research](RESULTS.md) · [evaluation contract](EVALUATION_CONTRACT.md).

**Status:** independent personal research portfolio. Not a completed client engagement, production-security certification, or proof of reduced real-world incidents.
