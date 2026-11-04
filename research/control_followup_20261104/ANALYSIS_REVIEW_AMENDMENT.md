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

## Component cross-runtime arithmetic and shared-source review

All 4,913 qualified component pilot/main trades were recomputed on Python 3.10
against the Python 3.12 frozen values. The maximum float difference was
4.618527782440651e-14; discrete disagreements and frozen-lock/row disagreements
were zero. Recomputed arithmetic uses the existing 1e-12 roundoff tolerance.
Frozen lock-to-row values and selected supplier/mode/grant remain exact.
The raw responses, forecasts, states and acceptance criteria do not change.

The preregistered component analysis used 24 authored-rule clusters. Review of
the original reused pools confirmed **12 shared historical source groups**.
`COMPONENT_REPRODUCTION.json` retains the original analysis. The separate
`REVIEWED_COMPONENT_ANALYSIS.json` uses the original group mapping, with source
file SHA provenance, for a post-hoc 12-source reanalysis. The primary estimands,
paired rows and four-way Holm family are unchanged; no new calls are made.
AR−GB net value remains −1.3559 (Holm4 p=.3574); supplier choice−fixed remains
−4.0148 (Holm4 p=.0293). Neither analysis establishes an AR advantage. This
review does not convert a post-hoc analysis into preregistered confirmation.
