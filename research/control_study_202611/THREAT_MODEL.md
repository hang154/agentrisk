# Threat model

Untrusted vendor/customer/CRM notes request changes in amount, target, ordering,
confirmation, data scope, or repeated execution. The actor receives a trusted
contract and must complete its legitimate task despite those notes. The attacker
does not change tool code, oracle code, authenticated receipts, or the protocol.
The actor cannot execute shell/Python, access hidden tests, change the gateway,
edit history, or contact real systems. This measures a bounded prompt-injection
mechanism, not robustness against an arbitrary adaptive adversary.

The mandatory tool gate and independent scorer use separate code paths. Hashes
detect accidental alteration inside the experiment; they are not remote hardware
attestation or proof against a compromised host. The same-model monitor is not a
stronger trusted commercial model, a human reviewer, or an independent organization.

Controls see only temporally available state. Verified outcomes may update B4 only
after execution; they cannot retroactively block it. Monitoring M2/M3 is explicitly
post-action detection. M0's missing receipt must not be interpreted as proof of
no unsafe execution. False blocks and UNKNOWN are first-class outcomes.

New-source independence is limited by shared semantic families and engine. Analyze
both source and family clustering; do not turn seeds/actions into independent tasks.
