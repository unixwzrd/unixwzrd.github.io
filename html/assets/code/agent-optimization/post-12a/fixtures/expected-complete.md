# Component Restart Review

Decision: READY FOR REVIEW
Evidence state: ready_for_review
Evidence captured: 2030-01-02 03:04:05 UTC
Target: demo-stack:model-proxy
Requested scope: cascade restart

## Observed target

- Lifecycle: running
- Health: healthy
- Observability: observed

## Canonical impact

- Target-only plan: restart demo-stack:model-proxy
- Cascade stop set: demo-stack:agent
- Observed running components within cascade impact: demo-stack:agent
- Restore order: demo-stack:agent

## Equivalent CLI argument array

["llmops", "component", "restart", "demo-stack:model-proxy", "--cascade"]

## Approval boundary

No command was executed. Captured status may have changed since 2030-01-02 03:04:05 UTC. Re-plan and re-observe through a separately qualified live adapter before any approved mutation.
