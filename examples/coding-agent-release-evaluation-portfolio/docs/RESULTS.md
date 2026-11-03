# Recorded coding-agent task and release results

100 derived tasks × two models × Single/Swarm × two seeds produced 800 recorded native attempts. Qwen resolved 238/400 attempts, with 44 unknown outcomes. GPT-OSS resolved 195/400, with 6 unknown outcomes. Both models recorded 108 unsafe scoped-release choices; a release choice is not an actual production incident.

[Native model/harness outcomes](../data/native_cells.csv) · [288 authority/control replay groups](../data/cells.csv) · [Risk Cells](../data/risk_cells.json)

The separate replay study grouped 147,456 policy/economic replay observations into 288 authority/control cells. Those are not 147,456 independent coding attempts. Positive-cost fractions in the replay are not automatically coding-error probabilities. This clean portfolio retains the workflow/control evidence rather than pricing artifacts.

Tasks were transformed from original coding issues for a fixed native runtime. They are not official SWE-bench leaderboard results. The eight local fixtures are scripted release-gate regressions, not fresh model inference.
