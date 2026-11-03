# Coding Agent QA | Patch, Release & Permission Gates — 60-second screen-recording plan

**Status:** storyboard only. **No video has been recorded.** Format: 1920×1080, silent captions or clear English narration, 60 seconds, no customer logos or invented testimonials.

| Timeline | Scene | Exact screen action | Suggested narration |
|---|---|---|---|
| 00–08 | Release decisions are a separate risk | Show the README and the difference between `patch passes CI` and `authorized release`. | A coding agent can produce a patch and still make a bad rollout decision. |
| 08–21 | Open an unsafe-but-plausible case | Open `fixtures/scenarios.json`; highlight `semantic-regression` and green public CI. | This scripted patch looks acceptable to a shallow CI check but fails semantic evidence. |
| 21–36 | Replay two release policies | Run `python3 evaluation.py demo`; highlight the baseline allow versus guarded `DENIED_EVIDENCE`. | The stricter mock release gate blocks the virtual rollout before state mutation. |
| 36–46 | Inspect false blocks and missing decisions | Point to `false_blocks`, `normal_success`, and `UNKNOWN`. | Preventing every deployment is not a successful automation policy. |
| 46–55 | Show native study separately | Open `docs/RESULTS.md`; show 238/400 and 195/400 resolved, plus 108 unsafe choices each. | The 800 native study attempts are not the 288 economic/authority replay groups. |
| 55–60 | Show exact handoff | Show `reports/SAMPLE_REPORT.md`, evaluation checks, and client scope. | Reproducible release regression tests and failure triage, not a security certification. |

## Preparation

```bash
python3 evaluation.py demo
python3 evaluation.py verify
python3 -m unittest -v
python3 verify_release.py
```

Record in a clean local directory with no terminal secrets, internal SSH paths, browser account data or production endpoints visible. Keep labels **Scripted Offline Demo** and **Historical Synthetic Research** on screen when relevant. The commands do not perform new voice/model inference. Use the existing committed output and report only if an actual screen capture has not yet been made.

Do not overlay the 8 authored demo cases with a headline implying they were 4,900/5,000/800 fresh model inference calls. Include a brief visual pause for UNKNOWN and false blocks as well as safety successes. The final call to action should be an Upwork-scoped risk-evaluation pilot, not a guaranteed security audit.
