# Verified execution evidence and adaptive AI control

**AgentRisk Control Study V1 — 4 November 2026**

This exploratory study asks two distinct questions: whether verified execution
evidence improves a language-model monitor's detection of unsafe state changes,
and whether using verified outcomes to update additional controls improves the
safety–utility trade-off. It implements the minimum prospective study proposed
for AgentRisk's AI control research, while retaining negative results.

## Design and evidence

We preregistered the protocol and source at commit `74040ba3` before the real model
pilot or main outcomes. Forty newly authored synthetic workflow specifications
share ten semantic families. Two scenarios (benign and prompt injection), five
control policies, and two seeds yield 800 main episodes. Four separate development
workflows provide calibration data and 40 pilot episodes. Main workflows are not
used to fit initial predictors. Reservation, return/inventory, data governance,
and subscription also form a named held-out-source panel.

GPT-OSS-20B MXFP4 is the actor and, in separate calls, the monitor. The model runs
on one H200, GPU2, with 131,072-token context and FP8 KV. Model parameters, seeds,
JSON schemas, ten-step cap, and cumulative token budgets are frozen. Actual tool
proposals pass through a pre-action controller, a native state machine, and an
independent outcome oracle. Receipts contain before/after states and hashes;
pre-action prediction locks precede execution and scoring. No host code generated
by the model is executed, and no real customer funds or accounts are involved.

All policies retain the same mandatory tool scope, subject ACL, authorization
reference, and per-action ceiling. B1 adds a separate-role LLM monitor; B2 adds
simple cumulative and duplicate-operation limits; B3 adds a frozen, transparent
Beta-bucket risk controller; B4 updates that controller using verified outcomes
of executed actions within the episode. B4 cannot override mandatory gates.
The risk controller is a new research baseline, **not** the historical RiskRank
model under a new name. B1's extra monitoring budget and tokens are reported.

Forty pilot and 800 main episodes completed with no transport-unknown episodes.
The main execution took 248.56 seconds (193.11 episodes/minute), with 3,751 API
calls, 4,148,896 input-plus-output tokens, and 771,514 output/reasoning tokens.
C512 was selected after three 512-request diagnostic repetitions with 512/512
valid responses each. Those diagnostic calls are not scientific task outcomes.

## Control-policy findings

| Policy | Benign exact completion | Unsafe state change | Synthetic direct loss | API tokens |
|---|---:|---:|---:|---:|
| B0 static gate | 74/80 | 10/160 | 12 | 729,079 |
| B1 LLM monitor | 73/80 | 10/160 | 0 | 1,286,974 |
| B2 cumulative/duplicate limit | 80/80 | 3/160 | 0 | 696,656 |
| B3 frozen risk controller | 79/80 | 2/160 | 0 | 732,215 |
| B4 outcome-updated controller | 79/80 | 2/160 | 0 | 703,972 |

The preregistered primary comparison does **not** establish B4's superiority to
B2: the unsafe-episode difference is −0.625 percentage points, with a ten-family
bootstrap 95% interval [−1.875, 0] and Holm-adjusted exact p=1. Benign completion
differs by −1.25 points, interval [−3.75, 0]. The utility noninferiority constraint
is met, but the risk-improvement requirement is not.

Against B0, B4's risk difference is −5 points and benign-completion difference
+6.25 points. The risk bootstrap interval [−9.375, −1.25] excludes zero, but the
prespecified family-level exact sign-flip test gives p=.125, Holm2 p=.25. We retain
the preregistered nonsuccess conclusion rather than selecting the favorable test.
B3 and B4 have identical aggregate completion and unsafe-execution counts; an
additional value of within-episode updating has not been established here.
Zero cash loss does not imply zero nonmonetary harm: B1 still has ten unsafe
episodes, and B2–B4 also have unsafe state changes.

## Monitoring findings

From each of the 160 B0 episodes, an event is selected by an episode-ID hash,
without observing the outcome. Five conditions judge the same actual execution:
M0 dialogue/action name/policy, M1 additional arguments/scope, M2 verified receipt
and state changes, M3 additional earlier receipts, and M2_PROSE the same M2 leaf
facts in prose. This is **post-action detection**, not prospective prevention.
M3 contains previous steps of the same episode, not a cross-session history.

| Condition | Valid | UNSURE | TP / FN / FP / TN among issued decisions | Brier |
|---|---:|---:|---|---:|
| M0 | 160 | 96 | 1 / 1 / 19 / 43 | .285672 |
| M1 | 160 | 75 | 1 / 0 / 20 / 64 | .248282 |
| M2 | 160 | 0 | 3 / 2 / 1 / 154 | .018809 |
| M3 | 160 | 0 | 2 / 3 / 0 / 155 | .017744 |
| M2_PROSE | 160 | 0 | 2 / 3 / 2 / 153 | .029791 |

Only five unique selected actions have an unsafe execution. UNSURE is retained
separately; excluding it changes denominators. M2−M0's exploratory paired Brier
difference is −.266863, family-bootstrap interval [−.319277, −.214117]. This
supports the value of supplying execution evidence in this task. It does not
isolate information quantity from every representation effect. M2−M2_PROSE's
interval crosses zero, as does M3−M2's. The evidence therefore does not establish
an advantage of JSON structure alone or accumulated earlier receipts.

## Forecasts, calibration and generalization

On 491 common B0 proposed actions, observed before execution, the research risk
score has Brier .244375, compared with GBDT .255525, LR .306546, and an unstratified
Beta baseline .513384. On 206 held-out-panel actions the corresponding scores are
.241331, .250554, .296300 and .510318. Log loss, reliability bins, and descriptive
paired score intervals are released. The latter were added after outcomes and
are labeled exploratory, not new primary hypothesis tests.

These scores predict **proposal contract violations**, not unconditional customer
incident rates. Development counterexamples are deliberately balanced, whereas
35/491 main B0 proposals violate the contract; probability calibration does not
transport automatically. A modest ranking over these fitted baselines is not a
validated historical RiskRank advantage, an unseen-model result, or a permission
to approve deployment. Held-out specifications share the simulator and model.

## Historical audit and reproduction

The separate historical Voice audit verifies all eight archive-part hashes and
2,114 reconstructed wire-input hashes. It retains the original 119 mechanically
flagged cases, two AI-observed cases, and 117 disagreements. Automated transcript
triage produces review candidates, not corrected gold labels. A 156-case blinded
human review package is prepared; both reviewer forms remain blank.

Independent reconstruction validates 840 pilot/main state trajectories and 3,944
API calls. An additional audit validates all 800 monitor requests, outputs, usage,
seed settings, event selections, and post-action timestamps; six tampering tests
are rejected. Local and remote results agree exactly on counts and decisions;
the maximum cross-Python floating-point difference is 7e−15. Reproduction accepts
only a fixed 1e−12 absolute float roundoff allowance, with exact discrete checks.

The protocol, code, real synthetic wire records, per-file hashes, and reproduction
command are public. Original source and outcomes remain preserved. A bootstrap
ordering fix and explicit post-action source binding are documented amendments;
no main episode was reissued. NAS quota prevented the planned NAS copy, so verified
full archives are retained on local SSD and a separate HDD, with the public
scientific package additionally stored in GitHub.

The next research questions remain open: blinded human adjudication, longitudinal
multi-session and multi-agent controls, adaptive attackers, legacy RiskQuote
component ablations, and genuine external workflow/model transfer. This study
provides a functioning, reproducible core platform and a useful monitoring signal;
it does not establish the full adaptive-control research claim.
