# multi-agent-orchestrator

Focused plugin for selecting and operating multi-agent modes safely.

## Includes

- Skill: `multi-agent-orchestrator`
- Command: `/multi-agent-orchestrator:team-plan`

## Scope

- Planning and coordination only
- Not a code-review or security scanner replacement

## Mode and Model Policy

### MODE_DECISION

| Decision | Use when | Avoid when |
|---|---|---|
| `plan-first` | Team structure is unclear, risky parallel edits, broad refactors | Small routine tasks |
| `direct` | Clear task with low coordination risk | Ambiguous ownership or many dependencies |

### MODEL_DECISION

| Profile | Use for |
|---|---|
| `light` | Recon, inventory, quick planning iterations |
| `balanced` | Standard team runbook construction |
| `strong` | Complex decomposition, dependency-heavy planning |

### Required output

- `TEAM_DECISION`, `MODE_DECISION`, and `MODEL_DECISION` must all be present in `/multi-agent-orchestrator:team-plan` output.
