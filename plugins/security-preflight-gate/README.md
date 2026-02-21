# security-preflight-gate

Security governance plugin that classifies work risk and recommends execution boundaries.

## Includes

- Skill: `security-preflight-gate`
- Command: `/security-preflight-gate:risk-check`

## Scope

- Pre-execution governance and policy recommendations
- Complements, not replaces, code security scanners

## Mode and Model Policy

### MODE_DECISION

| Decision | Use when |
|---|---|
| `plan-first` | Risk tier is medium/high, unknown change impact, sensitive assets involved |
| `direct` | Low-risk and clearly bounded task |

### MODEL_DECISION

| Profile | Use for |
|---|---|
| `light` | Basic risk triage and policy reminders |
| `balanced` | Typical risk review with concrete guardrails |
| `strong` | High-risk threat modeling and strict governance recommendations |

### Security requirement

- Risk output must include both `MODE_DECISION` and `MODEL_DECISION` with rationale.
- Network governance should prefer `WebFetch` domain controls plus `PreToolUse` hooks over brittle Bash URL patterns.
