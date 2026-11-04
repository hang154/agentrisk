# Final analysis review

The raw organization receipts and outcome labels are unchanged. The first audit
reconstructed all 1,740 pilot/main teams and 28,046 calls. Review of its summary
identified two reporting issues, corrected in a separately versioned
`REVIEWED_INDEPENDENT_REPRODUCTION.json`:

1. `correct_invoices` in an UNKNOWN team is a count observed before interruption,
   not a completed-work result. Paired utility analysis now requires both teams
   to be known, as the other completion/loss endpoints already did. The seven
   original unknowns and observed partial states remain in the raw evidence.
2. A bootstrap over one shared mechanism returns a degenerate point interval.
   It cannot support between-workflow uncertainty. The primary cross-mechanism
   CI and p-value are withheld (`null`), retaining point effects and explicitly
   descriptive six-parameterization sensitivity intervals. No superiority claim
   can pass on this single mechanism.

This is a reporting correction, not a changed population, outcome, acceptance
threshold or favorable rerun. The earlier independent report is preserved.
Local/remote JSON comparisons normalize serialization; dictionary order and
tuple/list serialization are not scientific differences. Discrete quantities
remain exact, and float roundoff tolerance remains 1e-12.
