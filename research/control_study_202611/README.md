# Outcome-Grounded Adaptive AI Control

[Protocol](PROTOCOL.md) · [Threat model](THREAT_MODEL.md) · [Historical Voice audit](VOICE_AUDIT.md)

This study connects three questions: what the monitor can observe, how verified
outcomes affect the next control decision, and whether the result carries to newly
authored workflow families. Prior AgentRisk results remain separate.

The implementation includes 40 synthetic workflows in ten semantic families,
five policies, a real model API runner, independent state scoring, pre-action
forecast locks, immutable receipts, a post-action monitoring comparison and a
separate raw-evidence reconstruction. The planned main study has 800 episodes.

## Run CPU checks

Python 3.10+ standard library, no Docker or package installation required:

```bash
python3 -m unittest discover -s experiments/control_study_202611 -t . -v
```

The tests include positive/negative controls for every workflow, hard-gate bypass,
receipt mutation, future-information exclusion, unknown outcomes, duplicate POST
prevention, interrupted leases, five-policy execution semantics, independent state
reconstruction, clustered statistics and baseline scoring during abstention.

## Freeze a new study

```bash
python3 -c "from experiments.control_study_202611.protocol import initialize; initialize('/path/to/new/evidence')"
```

The existing frozen artifacts must not be overwritten. New task semantics or
scientific budgets require a new protocol and experiment version. Commit the
protocol before any main result. The launch/profile lock is additional evidence,
not a replacement for the protocol lock.

## Authorized GPU execution

GPU2 only after release of its existing workload. The production runner expects
the owned OpenAI-compatible GPT-OSS endpoint and existing approved runtime. A
guardian executes the real E2E/pilot, workload certification, main study, monitor
comparison, independent reconstruction and report in order. It halts on repeated
transport/semantic failure; unknown request IDs cannot be reposted. API concurrency
and CPU/IO work are bounded separately. Other services are not stopped by it.

Current launch status is recorded in `artifacts/control_study_202611/IMPLEMENTATION_STATUS.json`.
CPU tests and a queued execution do not mean the GPU experiment has completed.

## Recompute real results

When the run publishes its evidence package:

```bash
python3 scripts/reproduce_control_results.py /path/to/evidence
```

This checks recorded requests/responses, token use and independent state outcomes
before rebuilding tables. It does not replace real model calls with fixtures.
`scripts/generate_control_results.py` produces the Korean report, CSV, comparisons
and SHA manifest from completed evidence.

The code follows separate setting/policy/monitor/scorer boundaries and exports
ordinary JSON trajectories. Native ControlArena plugin interoperability is not
yet certified. Long-term multi-session organizations, adaptive attackers and
RiskQuote factor decomposition remain separately scoped extensions.
