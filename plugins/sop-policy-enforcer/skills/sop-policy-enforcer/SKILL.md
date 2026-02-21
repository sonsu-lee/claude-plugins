---
name: sop-policy-enforcer
description: Enforce SOP checkpoints and block completion when required evidence is missing.
version: 0.1.0
---

Assess the task lifecycle in three stages:

1. Start
- Scope, constraints, and planned evidence
- MODE_DECISION logged (`plan-first` or `direct`) with rationale
- MODEL_DECISION logged (`light`, `balanced`, `strong`) with rationale

2. In progress
- Drift from scope
- Missing verification steps

3. Completion
- Acceptance criteria met or not
- Evidence status
- Required remediation
- Governance traceability: mode/model rationale must be present and consistent
- If `plan-first` was required, confirm implementation followed approved plan

If requirements are not met, output `BLOCKED` and exact next actions.
