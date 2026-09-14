# Component Triage

Use this skill when an operator needs a review packet for a proposed cascading component restart and has supplied one already-sanitized evidence envelope conforming to `schemas/evidence-envelope.schema.json`.

Validate the envelope before interpretation. Treat the captured target-only and cascade plans as the canonical plan evidence. Correlate status only with component membership already present in that cascade plan; never infer or rediscover dependencies. Report missing, unreachable, unobserved, inconsistent, or stale evidence as not ready.

Show the equivalent operation only as a validated argument array. Never construct shell text, execute the array, call an installed control plane, open a network connection, search the filesystem, retrieve a secret, or expose a captured command string. `READY FOR REVIEW` means that the captured evidence is internally consistent enough for human review. It does not mean approved, current, or executed.
