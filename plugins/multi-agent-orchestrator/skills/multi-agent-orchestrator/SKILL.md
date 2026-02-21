---
name: multi-agent-orchestrator
description: Build a multi-agent runbook with mode selection, decomposition, ownership, and cleanup.
version: 0.1.0
---

Produce an orchestration runbook with:

1) Team suitability gate
- Decide if `agent-teams` is appropriate.
- For sequential or same-file-heavy work, prefer `single-session` or `subagents`.

2) Mode selection
- Choose one: `single-session`, `subagents`, `agent-teams`.
- Include rationale tied to coordination overhead and expected parallel value.

3) Plan and model decisions
- Add `MODE_DECISION`: `plan-first` or `direct` with rationale.
- Add model profile by task: `light`, `balanced`, or `strong`.

4) Task decomposition
- 3-8 atomic tasks with file ownership per task.
- Include expected output for each task.

5) Execution policy
- Delegate mode recommendation.
- Check-in frequency and escalation policy.
- Plan approval requirement before implementation when risk is high.

6) Completion and cleanup
- Completion sequence and cleanup steps.
- Limitation fallback for stale task states and delayed shutdown.

Minimize coordination overhead and avoid same-file parallel edits.
