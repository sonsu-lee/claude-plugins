# Governance

Unified governance plugin — orchestration runbooks, security risk gates, and SOP policy enforcement. Covers the full task lifecycle: preflight checks before execution, policy compliance during progress, and evidence verification at completion.

**For:** Claude Code users running multi-step tasks, agent teams, or any work that benefits from structured risk assessment and completion verification.

## What This Does

### Without this plugin
> "Refactor the auth module across 8 files" → Claude jumps straight in, no risk assessment, no execution plan, no completion check

### With this plugin
> "Refactor the auth module across 8 files" → Claude runs a preflight gate (risk: medium, mode: plan-first, model: balanced), produces an orchestration runbook with file ownership boundaries, and validates evidence before reporting done

---

## Skills

### Orchestrator — Multi-Agent Runbooks

Triggers when tasks involve agent teams, subagents, or parallel execution.

Decides execution mode (single-session vs subagents vs agent-teams), decomposes tasks into 3-8 atomic units with file ownership, and produces a cleanup/fallback plan.

```
"Set up a team to build the new dashboard feature"
"Should I use subagents or agent-teams for this refactor?"
```

### Risk Gate — Security Preflight

Triggers when tasks touch permissions, sandbox config, sensitive paths, or external services.

Classifies risk (low/medium/high), recommends permission mode and sandbox constraints, and returns a GO / CONDITIONAL-GO / NO-GO decision.

```
"Deploy the updated API handler to production"
"Modify the CI pipeline configuration"
```

### Policy Check — SOP Enforcement

Triggers at task lifecycle boundaries (start, in-progress, completion).

Validates scope compliance, evidence completeness, and governance traceability. Blocks completion when required evidence is missing.

```
"Am I ready to mark this task as done?"
"Check if I've drifted from the original scope"
```

## Commands

### Composite Commands

| Command | Description |
|---------|-------------|
| `/governance:preflight <task>` | Run all pre-execution checks (orchestration + security + policy) in one pass |
| `/governance:ops-check [what changed]` | Run completion verification before reporting done |

### Individual Commands

| Command | Description |
|---------|-------------|
| `/governance:team-plan <task goal>` | Generate an orchestration runbook |
| `/governance:risk-check <task summary>` | Classify risk and return execution conditions |
| `/governance:sop-check <stage> <task>` | Run SOP compliance for a specific lifecycle stage |

## Typical Workflow

```
1. /governance:preflight "refactor auth module"
   → GO, plan-first, balanced, agent-teams with 4 tasks

2. (execute the work)

3. /governance:ops-check "refactored auth into service layer"
   → PASS or FAIL with remediation actions
```

## Components

| Component | Type | Purpose |
|-----------|------|---------|
| `orchestrator` | Skill | Execution mode selection + task decomposition |
| `risk-gate` | Skill | Risk classification + permission/sandbox recommendations |
| `policy-check` | Skill | SOP checkpoint enforcement across task lifecycle |
| `/governance:preflight` | Command | Composite pre-execution gate |
| `/governance:ops-check` | Command | Completion verification |
| `/governance:team-plan` | Command | Orchestration runbook generation |
| `/governance:risk-check` | Command | Security risk classification |
| `/governance:sop-check` | Command | SOP compliance check |

## Key Concepts

| Concept | Values | Description |
|---------|--------|-------------|
| MODE_DECISION | `plan-first` / `direct` | Whether to plan before implementing |
| MODEL_DECISION | `light` / `balanced` / `strong` | Model capability needed for the task |
| TEAM_DECISION | `single-session` / `subagents` / `agent-teams` | Execution parallelism strategy |
| Risk tier | `low` / `medium` / `high` | Task risk classification |
| Gate result | `GO` / `CONDITIONAL-GO` / `NO-GO` | Preflight decision |
| Policy result | `PASS` / `BLOCKED` | SOP compliance status |
