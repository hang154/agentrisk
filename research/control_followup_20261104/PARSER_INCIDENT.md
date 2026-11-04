# GPT-OSS Harmony terminal incident

The organization run hit seven HTTP500 responses with `Unexpected token 200002 while expecting start token 200006`. The runtime traceback points to `HarmonyParser.process_chunk`, not a GPU memory failure. The fail-closed client then stopped admission, leaving 1,563 team records marked UNKNOWN, including work that never reached POST. The seven failed requests are immutable and will never be reissued. Pending admission must be distinguished from a dispatched unknown.

Upstream issue: https://github.com/vllm-project/vllm/issues/50690 . Local parser lacks trailing-error handling. Token200002 is `<|return|>`,200007 is `<|end|>`. An owned-server wrapper may recover **only** the exact trailing sequence end/return after a complete JSON answer; other errors still fail. It retains original output token IDs and parser errors and does not change generation, budgets, seed, reasoning or usage accounting. No shared runtime files are edited.

Continuation creates new immutable result records referencing original partial records. It reuses actual old responses, dispatches only IDs proven never posted, and excludes seven roots with an actual unknown response from automatic continuation. Original UNKNOWN records remain unchanged. A new runtime stratum and real canary are required; post-fix results must not be described as an entirely clean original run.
