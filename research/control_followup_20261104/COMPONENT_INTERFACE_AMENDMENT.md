# Required-schema visibility amendment, before main dispatch

The first 17 component pilot trades made 68 real calls, with zero HTTP unknowns.
Two reviewer responses reached 4,096 output tokens while repeating the `reason`
string. The trace explicitly showed uncertainty about which JSON fields were
required: structured decoding constrained final output, but the role prompt did
not expose the schema. Both malformed outputs, their usage and all 17 original
pilot trades are preserved under `components`. No main trade was dispatched.

`component-schema-v2` includes the identical JSON schema in every role's system
message and requests one concise, nonrepeating explanation. It does not change
the output cap, reasoning effort, sampling, context, scientific population,
candidate list, forecast models, gates, oracle or outcome criteria. All main
conditions use this same amended interface. This is a new interface stratum,
not a claim that the original pilot passed.

New independent pilot seeds 8200–8216 and versioned request IDs cannot overwrite
or retry original requests. The 17-policy E2E gate must pass before the same
4,896-trade main grid (seeds8101/8102) starts. Original bad pilot outcomes are
excluded from scientific analysis but included in the failure/evidence archive.

The final report retains interface failures and distinguishes schema correctness
from business correctness. No success-driven extension or changed statistical
acceptance threshold is permitted.
