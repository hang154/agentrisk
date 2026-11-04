# Control Study follow-up: reviewed evidence and reproducibility

[한국어 결과](RESEARCH_FINDINGS_KO.md) · [English brief](RESEARCH_BRIEF_EN.md) ·
[최종 상태](../../artifacts/control_followup_20261104/FINAL_STATUS.json) ·
[실행 계획](PROTOCOL.md)

The follow-up completes the retrospective monitor census, prescribed multi-agent
and multi-session experiment, bounded development attacker, historical predictor
support/parity checks, RiskQuote component factorial, and trajectory export.
Human double review was explicitly skipped by the user. Execution completion is
separate from positive hypothesis confirmation; unknowns and failed pilots remain.

## Reproduce without a GPU or network calls

From this repository, use Python 3.10+ and an SSD directory with approximately
6 GB free and 600,000 available inodes. The scripts use the standard library.
No model, Docker, package installation or paid API is needed for reanalysis.

```bash
python3 scripts/extract_control_followup.py --destination /tmp/agentrisk-followup-reproduction
python3 scripts/reproduce_control_followup.py \
  --evidence /tmp/agentrisk-followup-reproduction \
  --v1 /tmp/agentrisk-followup-reproduction/evidence \
  --output /tmp/agentrisk-followup-reproduction/check.json
python3 scripts/export_control_tables.py \
  --evidence /tmp/agentrisk-followup-reproduction \
  --output /tmp/agentrisk-followup-reproduction/tables
python3 -m unittest discover -s experiments/control_followup_20261104 -t .
```

Archive SHA-256 digests are in
[PUBLIC_ARCHIVES.json](../../artifacts/control_followup_20261104/PUBLIC_ARCHIVES.json).
The extractor rejects paths outside its destination, links and nonregular files;
it checks archive digests and available per-member manifests before analysis.
Existing files must match exactly. It never silently replaces existing evidence.
The original V1 archive is reused as the source population for the monitor census.

The independent audit reconstructs actual state transitions and scoring from
raw responses, contracts and pre-action locks. It checks the complete grid,
seeds, cumulative output budgets, raw token usage, role inputs, invalid output
accounting, typed histories and forecast ordering. It does not issue model calls.
Discrete results match exactly; float comparisons allow only 1e-12 roundoff.

## Evidence layout

| Directory | Meaning |
|---|---|
| `evidence` | Original V1 public evidence, unchanged |
| `census` | 2,455 retrospective judgments; 800 reused, 1,655 new |
| `attacker` | Eight generated notes and 24 development probe episodes |
| `organizations` | Original organization run, including failures and stopped admission |
| `organizations_continuation` | New result records, preserved prior responses, only never-POSTed work continued |
| `components` | Failed original interface pilot: 17 trades, 68 calls |
| `components_schema_v2` | Qualified new pilot and 4,896 main trades |
| `parser_runtime_evidence` | Exact terminal-token exceptions and bounded recoveries |
| `parser_canary` | Seven distinct interface diagnostics, never scientific samples |

The public package includes synthetic research records. Historical private Voice
transcripts and host credential files are not part of this release. The prior
Voice audit and human-review waiver remain separately referenced.

## Trajectory interchange

`experiments/control_followup_20261104/trajectory_export.py` exports the pinned
[ControlArena directory-writer field contract](https://github.com/UKGovernmentBEIS/control-arena/blob/eb1494f042d0d587e3a2c3c88fc5416d1d8edc02/control_arena/export/writers/directory.py).
Each actual request retains its message segment, hashes, usage and finish reason.
Null final content and reasoning-only/truncated responses are preserved. Oracle
and state labels appear only as post-action metadata. Separate actor contexts
are not misrepresented as one uninterrupted conversation.

This is a verified interchange export, not certification of an installed native
ControlArena plugin or an Inspect `.eval` run. Full export archives and validation
receipts are included separately from the evidence required for score reproduction.

## Amendments and preserved failures

- [Parser incident and safe continuation](PARSER_INCIDENT.md)
- [One-mechanism lineage correction](LINEAGE_AUDIT_AMENDMENT.md)
- [Required-schema visibility before component main](COMPONENT_INTERFACE_AMENDMENT.md)
- [Known-only utility analysis and single-mechanism uncertainty](ANALYSIS_REVIEW_AMENDMENT.md)

GPU2 remains on its owned GPT-OSS service. This repository does not contain SSH
credentials or a command that stops unrelated services. Live execution requires
the recorded model/runtime contract and explicit access to the intended host;
the reproducibility commands above only perform CPU reanalysis.

The final review preserves the preregistered 24-rule component analysis and adds
a separately labeled 12-shared-source analysis from the original historical
pool provenance. Both calculations are included in the public reproduction.
