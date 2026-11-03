# Voice AI Agent Red Teaming & Tool-Action QA — 60-second screen-recording plan

**Status:** storyboard only. **No video has been recorded.** Format: 1920×1080, silent captions or clear English narration, 60 seconds, no customer logos or invented testimonials.

| Timeline | Scene | Exact screen action | Suggested narration |
|---|---|---|---|
| 00–08 | Voice agent attack surface | Show the README and a short `transcript → tool proposal → permission gate` chain. | A voice assistant hears customer speech. Which instructions should it trust? |
| 08–21 | Show adversarial vs legitimate transcripts | Open `fixtures/scenarios.json`; highlight the transcript and refund action on a normal and an override case. | Caller speech is untrusted input; it cannot raise an approved refund amount. |
| 21–36 | Replay control decisions | Run `python3 evaluation.py demo`; highlight `DENIED_AMOUNT`, `state_changed=false` and `synthetic_loss`. | The guarded mock action is blocked before the virtual ledger changes. |
| 36–46 | Demonstrate evaluation integrity | Show `UNKNOWN`, `false_blocks` and `normal_success` in the demo output. | A useful test must report missed decisions and normal-call friction too. |
| 46–55 | Show research trade-off | Open `docs/RESULTS.md`; show 66/1664 vs 0/1679 and 232/452 vs 211/440. | These are historical synthetic TTS/ASR experiments, not live customers or this demo. |
| 55–60 | Offer a client QA package | Show `docs/UPWORK_PORTFOLIO.md` and sample report. | The handoff is a repeatable call-level risk test and retest plan. |

## Preparation

```bash
python3 evaluation.py demo
python3 evaluation.py verify
python3 -m unittest -v
python3 verify_release.py
```

Record in a clean local directory with no terminal secrets, internal SSH paths, browser account data or production endpoints visible. Keep labels **Scripted Offline Demo** and **Historical Synthetic Research** on screen when relevant. The commands do not perform new voice/model inference. Use the existing committed output and report only if an actual screen capture has not yet been made.

Do not overlay the 8 authored demo cases with a headline implying they were 4,900/5,000/800 fresh model inference calls. Include a brief visual pause for UNKNOWN and false blocks as well as safety successes. The final call to action should be an Upwork-scoped risk-evaluation pilot, not a guaranteed security audit.
