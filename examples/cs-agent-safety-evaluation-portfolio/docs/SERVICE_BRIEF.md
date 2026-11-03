# Client-facing service brief — CS Agent Risk & QA Evaluation

**Target buyer:** AI support vendors, ecommerce CX teams or agent developers preparing to automate refunds, account changes, cancellations or policy-sensitive workflows.

**Problem:** A chatbot can generate a plausible answer while proposing a duplicate refund, exceeding an authorized amount, using the wrong account or blocking legitimate work. Response-only accuracy does not verify a completed business action.

## Deliverables for an initial fixed-scope pilot

1. **Boundary and oracle specification:** one selected workflow, trusted business rules, allowed tool actions, required identity/amount/approval evidence and independent correct-state definition.
2. **30–50 approved evaluation cases:** frozen normal, exception and adversarial scenarios; anonymized traces or approved mock inputs.
3. **Action-level evaluation harness:** safe offline replay with attempted tool action, gate receipt, expected vs observed virtual state and UNKNOWN outcomes.
4. **Comparison report:** baseline versus one guarded condition, correct completion, unsafe state mutations, false blocks, inconclusive cases and investigation priority.
5. **Retest handoff:** runnable checks, documented fixes, one agreed retest comparison and limitations.

**Customer input:** current workflow policy, approved synthetic or de-identified examples, what tool side effects are possible, and who signs off on acceptance.

**Not included in this scope:** real refunds, production mutations, formal penetration-test attestation, training a new LLM, 24/7 monitoring, or a guarantee that attacks cannot succeed. Live adapters and vendor-specific APIs require separate authorization and scope.

## Evaluation acceptance criteria

All frozen scenarios receive traceable verdicts. Unsafe *proposals* are kept distinct from *executed actions*. Missing results do not become 0% risk. The normal-task metric and false-block metric are reported alongside unsafe-action counts. Fixes are tested against the **same** frozen cases.

## Example proposal text

I can help evaluate your support agent at the tool-action level rather than relying only on answer-quality scores. I would start with one refund or account-change workflow, freeze 30–50 approved cases, replay your current and guarded configurations, then deliver a ranked findings report and deterministic regression tests. My portfolio is an offline research demo with clearly labelled synthetic evidence, not a claim of previous customer engagements. What actions can your agent currently execute, and how do you confirm an action was authorized?

[Upwork portfolio wording](UPWORK_PORTFOLIO.md) · [Sample report](../reports/SAMPLE_REPORT.md) · [Evaluation contract](EVALUATION_CONTRACT.md)
