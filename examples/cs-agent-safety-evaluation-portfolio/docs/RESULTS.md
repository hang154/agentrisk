# Historical CS task and tool-safety results

Legacy study: 4,900 synthetic episodes across seven policy conditions. The legacy workflow aggregates remain in `data/legacy_cells.csv`, separate from the newer 224 customer-case Risk Cells.

In the newer normal-case training summaries, Gemma B0 recorded 1,842/5,040 correct customer cases and 995 state errors; B3 recorded 1,864/5,040 and 362 errors. Qwen B0 recorded 2,028/5,040 and 339 errors; B3 recorded 2,162/5,040 and 90 errors. B0 retains existing hard gates; B3 combines task scope and reviewer. Neither this comparison nor a repeated policy view is a collection of independent production incidents.

[Customer-case summaries](../data/summary.csv) · [Public Risk Cells](../data/risk_cells.json)

Legacy reservation/returns outcomes use the original study's proxy oracle. They are not silently relabelled as independent reservation/RMA evaluations. Customer-case and episode denominators remain separate.

The runnable eight-case demo is authored offline regression data. It is not a new LLM run. Unknown outcomes remain unknown; useful-work completion is shown beside unsafe actions.
