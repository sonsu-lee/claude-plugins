---
description: Run pre-execution governance checks (orchestration, security, policy)
argument-hint: <task summary>
---

You are running a preflight governance check for:

`$ARGUMENTS`

Perform five checks and return concise output:

0) Plan Mode gate
- Decide `MODE_DECISION`: `plan-first` or `direct`.
- Use `plan-first` when scope is unclear, change spans multiple files, or risk is high.
- Use `direct` for small, clearly-scoped changes.

1) Orchestration choice
- single-session vs subagents vs agent-teams

2) Model routing
- Decide `MODEL_DECISION`: `light`, `balanced`, or `strong`.
- `light`: codebase search, summarization, checklist updates.
- `balanced`: implementation with normal complexity.
- `strong`: architecture tradeoffs, complex debugging, high-risk changes.

3) Security gate
- risk tier, permission mode, sandbox requirement

4) Policy gate
- required checkpoints and evidence expectations

Output format:
- Decision: GO or CONDITIONAL-GO
- MODE_DECISION: plan-first or direct
- MODEL_DECISION: light, balanced, or strong
- Why: brief rationale for mode/model decisions
- Required conditions (if any)
- First execution step
