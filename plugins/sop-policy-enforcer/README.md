# sop-policy-enforcer

SOP-focused plugin for enforcing checkpoints across task lifecycle.

## Includes

- Skill: `sop-policy-enforcer`
- Command: `/sop-policy-enforcer:sop-check`

## Scope

- Process compliance and completion evidence checks
- Not a replacement for project-specific lint/test tooling

## Mode and Model Policy

### MODE_DECISION

| Decision | Policy expectation |
|---|---|
| `plan-first` | Start-stage logs must include approved plan linkage before implementation |
| `direct` | Start-stage logs must justify why planning overhead is unnecessary |

### MODEL_DECISION

| Profile | Policy expectation |
|---|---|
| `light` | Allowed for low-risk checks and checklist validation |
| `balanced` | Default for regular compliance reviews |
| `strong` | Required for high-risk completion gates |

### Compliance requirement

- `/sop-policy-enforcer:sop-check` should treat missing mode/model rationale as `BLOCKED` until corrected.
