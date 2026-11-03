# Client-facing service brief — Voice Agent Red Teaming & QA

**Target buyer:** voice-agent builders and operators of appointment, reservation, billing or call-center agents with tool access.

**Problem:** Untrusted caller transcripts may attempt to override business rules, create a payment/refund action, or bypass identity checks. A call may also be incorrectly escalated or blocked while doing legitimate work.

## Fixed-scope evaluation pilot

1. Select one call flow and explicitly enumerate tool scopes, authentication, amount rules, handoff conditions and acceptable state transitions.
2. Agree on 30–50 synthetic or consented/de-identified transcript scenarios, including normal callers and adversarial instructions.
3. Freeze expected outcomes **before** evaluation. Review recorded transcripts or approved model/tool traces in an isolated test context.
4. Compare one current configuration to one stronger tool-boundary policy on the same cases.
5. Deliver attempted vs passed tool actions, correct handoffs, false blocks, UNKNOWN, evidence excerpts, remediation recommendations and reproducible retest cases.

**Input required:** call-flow specification, available tool names/actions, voice recording permissions if applicable, an approved test endpoint or sanitized logs. No recordings or live integration are requested just to discuss scope.

**Not included:** guaranteed safety, unrestricted calling of public telephone numbers, full telephony/ASR integration or live payment execution. New TTS/ASR/LLM inference is an optional, separately authorized engagement.

## Acceptance

The normal and adversarial cases use a consistent oracle. Attack attempts are not counted as successful tool executions. Case failures and missing responses remain in the denominator. The report includes normal-caller utility alongside defense performance.

## Proposal sample

I can evaluate whether your voice AI handles adversarial caller instructions at the tool boundary while completing legitimate calls. I would agree on one call flow, freeze 30–50 approved transcripts/cases and compare current versus guarded settings using independent expected outcomes. You would receive a trace-level findings report, false-block analysis and regression tests. My included demo is an offline replay, whereas the linked TTS/ASR outcomes are a separate synthetic research study. Could you share the tool actions your phone agent is allowed to execute and your existing QA criteria?

[Upwork portfolio wording](UPWORK_PORTFOLIO.md) · [Sample report](../reports/SAMPLE_REPORT.md) · [Study limits](RESULTS.md)
