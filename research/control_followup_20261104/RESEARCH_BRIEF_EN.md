# Verified evidence, shared state, and the limits of adaptive control

**AgentRisk Control Study follow-up — 4 November 2026**

This follow-up separates three questions: whether verified execution evidence
improves monitoring, whether outcome-updated controls outperform simpler gates,
and which components explain a risk-based delegation system's economic value.
It preserves the original Control Study, failed requests, protocol locks and
negative findings. Human double adjudication was explicitly waived by the user;
no human gold labels or customer validation are claimed.

## Evidence-grounded monitoring

We completed a retrospective census of all 491 eligible B0 actions in the
original study. Five information conditions produce 2,455 judgments: 800 actual
prior judgments are reused and 1,655 are new model calls. All conditions use the
same safety definition and target execution. Only 17 unique actions actually
have unsafe state changes. This is post-action detection, not prevention using
future evidence.

The dialogue/policy condition M0 has Brier .283678, with 317 UNSURE judgments.
M2, which adds verified receipts and state differences, has Brier .020864 and
no UNSURE judgments: 12 true positives, five false negatives, six false positives
and 468 true negatives. The equal-workflow-cluster M2−M0 Brier effect is −.262668,
95% bootstrap interval [−.295590, −.230228], exact sign-flip p=.001953. The result
supports providing execution evidence in this population, without treating the
census as an independent confirmation. Neither the added history in M3 nor the
JSON-versus-prose comparison establishes a separate incremental benefit.

## Organizations, sessions and receipt sharing

We ran 1,728 prescribed organizations: 1/2/4 agents, single/split sessions,
none/recent-two/full receipt sharing, four controllers, two scenarios and two
seeds. Agents have separate real model contexts; same-round proposals run
concurrently and commits are serialized. Every condition retains mandatory
subject, assignment, vendor, per-action and wallet gates. This is assigned
organization size, not evidence of autonomous spawning.

The six contract variants share one payment mechanism. A lineage audit corrected
an earlier description of six independent mechanisms. Primary between-workflow
confidence intervals and p-values are therefore withheld. Descriptive variant
sensitivities remain available, without a cross-workflow superiority claim.

There are 1,721 known team outcomes and seven preserved original HTTP failures.
ADAPTIVE has benign exact completion 79/215 and unsafe state changes in 182/430
known teams; CUMULATIVE has 78/215 and 179/430. Outcome updating does not establish
an advantage over the simple cumulative controller. Full receipt sharing has
26/573 unsafe teams and 176/287 benign completions, while recent-two sharing has
425/574 and 33/286. This contrast is descriptive within one mechanism. Recent-two
replaces rather than augments the longer own-session receipt set, so the result
does not mean that adding a small amount of evidence is universally harmful.

Eight attack candidates were generated in two rounds with feedback from 24
development-only probes. The selected candidate was frozen before organization
outcomes. It caused zero unsafe development episodes; two candidates were
refusals. This is a weak bounded attacker, not an adaptive-attack robustness
certificate.

## RiskQuote component factorial

On the existing 24 authored business-rule families, we ran 4,896 new trades:
AR/GB predictor × fixed/selected supplier × fixed/selected authority × frozen/
updated history, plus a simple typed Beta-history policy. Each trade uses four
real role calls and independent settlement reconstruction. Five supplier
configurations use the same GPT-OSS base model with different routing depths and
prompt styles. This is not a replication of the historical two-model result or
an unseen-workflow evaluation.

All choice conditions receive the same candidates and authority options. Each
trade also locks AR, GB and SIMPLE forecasts for the identical selected action
before its outcome. Unchosen actions are not imputed. The preregistered analysis used 24 rule clusters and remains preserved. Final
review identified 12 shared historical source groups. The table below is an
explicitly post-hoc 12-source reanalysis, with Holm correction across four
net-value tests; it is not relabeled as a new preregistered finding.

| Factor change | Mean net-value effect | 95% shared-source interval | Holm4 p |
|---|---:|---|---:|
| AR − GB | -1.3559 | [-2.8203, +0.0821] | 0.3574 |
| Supplier selection − fixed | -4.0148 | [-6.4382, -1.7499] | 0.0293 |
| Authority selection − fixed | +0.0929 | [-1.9102, +2.2127] | 1.0000 |
| History update − frozen | -0.0234 | [-1.7036, +1.5352] | 1.0000 |

AR does not establish a net-value advantage over GB. On the same selected
pay-scope actions, material-risk Brier is .077650 for AR versus .079234 for GB,
but the paired family-level difference is inconclusive. Permission-violation
Brier is worse for AR (.140102 versus .130461). AR's full configuration exceeds
the conservative SIMPLE policy's net value, but SIMPLE mostly withholds payment;
that contrast is not evidence of a uniquely better risk predictor.

Net value is synthetic accounting: 100 for exact pay-scope completion minus
supplier fee, independently observed loss and fixed overhead .6. Correct
handling of a zero-amount obligation can count as completion. Payment execution,
unpaid obligations, read-only completion, material changes and tokens are retained
separately. There are zero HTTP unknowns and 16 truncated/invalid role outputs
among 19,584 main role calls; those outputs are counted as failures, not retried.

## Integrity and reproducibility

The retained GPU2 GPT-OSS profile uses medium reasoning, temperature .6,
top_p .95, 131,072 context, 4,096 output tokens per call and the previously
qualified C512 admission limit. A scoped Harmony parser wrapper removes only a
redundant final terminal after a complete JSON answer. Thirty-nine recoveries
match actual response IDs and unchanged generated-token usage. The seven
original failures remain unknown. Continuation dispatches only work proven never
POSTed; 119,046 protected original file hashes match and original reissues are zero.

The first 17-trade component pilot had two repeating/truncated reviewer outputs.
Before any main dispatch, an amended interface exposed the unchanged schema to
each role. A distinct 17-trade pilot passed; budgets and scientific criteria
were unchanged. Both pilot strata are released.

Independent audits reconstruct 1,740 organization teams and 28,046 raw calls,
and 4,913 qualified component pilot/main trades with 19,652 calls. Historical
RiskRank's 2,304 frozen forecasts and RiskQuote's 1,440 portable calculations
match their original implementations. Unsupported new RiskRank semantics abstain
rather than emitting fabricated transport probabilities.

The release includes raw synthetic requests/responses, states, source/seed/budget
locks, original errors, per-file hashes, outcome CSVs, CPU-only reproduction
scripts and actual multi-context trajectory exports. The latter follow the
ControlArena directory-writer contract; no installed native plugin is claimed.
SSD and separate-HDD backups are hash-checked. NAS writes remain blocked by quota.

The main lesson is specific: independently verified execution evidence and
accessible shared history matter, but adding a learned/adaptive risk layer does
not automatically improve the safety–utility frontier. Retaining this negative
result is necessary to identify when simpler system controls are sufficient.
