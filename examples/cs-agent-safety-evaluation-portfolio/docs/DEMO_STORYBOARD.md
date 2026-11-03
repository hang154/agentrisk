# Customer Support AI Agent QA & Tool Safety — 60-second screen-recording plan

**Status:** storyboard only. **No video has been recorded.** Format: 1920×1080, silent captions or clear English narration, 60 seconds, no customer logos or invented testimonials.

| Timeline | Scene | Exact screen action | Suggested narration |
|---|---|---|---|
| 00–08 | Customer task and risk: correct refund vs over-refund | Show README hero and an allowed vs unauthorized refund diagram. | Can this support agent resolve the request without paying more than it should? |
| 08–21 | Read normal and abnormal customer-action fixtures | Open `fixtures/scenarios.json`; compare `normal-refund` and `over-refund`. | The agent can propose an action, but permission to call a tool is not transaction authorization. |
| 21–36 | Run deterministic evaluation | Run `python3 evaluation.py demo`; highlight `DENIED_AMOUNT` and `state_changed=false`. | The guarded path rejects an excessive refund before any virtual state change. |
| 36–46 | Show utility and missingness | Highlight `normal_success`, `false_blocks`, `material_errors` and `UNKNOWN` in the output. | We measure useful work and harmful actions together. Unknown stays unknown. |
| 46–55 | Show recorded research evidence | Open `docs/RESULTS.md`; point to Gemma and Qwen B0/B3 state-error figures. | The research tables are historical synthetic model runs; this short demo is scripted. |
| 55–60 | Offer a scoped client deliverable | Show `reports/SAMPLE_REPORT.md` and `docs/UPWORK_PORTFOLIO.md`. | A fixed scenario suite, prioritized findings and retestable checks. |

## Preparation

```bash
python3 evaluation.py demo
python3 evaluation.py verify
python3 -m unittest -v
python3 verify_release.py
```

Record in a clean local directory with no terminal secrets, internal SSH paths, browser account data or production endpoints visible. Keep labels **Scripted Offline Demo** and **Historical Synthetic Research** on screen when relevant. The commands do not perform new voice/model inference. Use the existing committed output and report only if an actual screen capture has not yet been made.

Do not overlay the 8 authored demo cases with a headline implying they were 4,900/5,000/800 fresh model inference calls. Include a brief visual pause for UNKNOWN and false blocks as well as safety successes. The final call to action should be an Upwork-scoped risk-evaluation pilot, not a guaranteed security audit.
