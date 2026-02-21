---
description: Run completion governance check before reporting done
argument-hint: [what changed]
---

Run a completion check for:

`$ARGUMENTS`

Validate:

1) Scope compliance
- No out-of-scope work

2) Evidence completeness
- Diagnostics/tests/build output coverage

3) Governance traceability
- Plan Mode rationale present (`plan-first` vs `direct`)
- Model selection rationale present (`light`/`balanced`/`strong`)
- If plan-first was required, confirm implementation followed approved plan

4) Operational closure
- Follow-up items and cleanup status

Output format:
- Result: PASS or FAIL
- Missing evidence (if fail)
- Missing governance logs (if fail)
- Remediation actions
