---
name: security-preflight-gate
description: Evaluate task risk and return safe permission/sandbox/hook recommendations.
version: 0.1.0
---

For each request, output:

- Risk tier: low/medium/high
- MODE_DECISION: plan-first/direct recommendation and reason
- MODEL_DECISION: light/balanced/strong recommendation and reason
- Permission posture: default/acceptEdits/plan/dontAsk recommendation
- Sensitive path deny list suggestions
- Ask-only command suggestions
- Sandbox recommendation and domain constraints
- Proceed conditions (`GO` or `CONDITIONAL-GO`)

Guardrails:
- Do not depend on Bash URL patterns alone for network governance.
- Prefer WebFetch domain controls and PreToolUse hooks when URL controls are required.
- Treat sandbox and permissions as complementary controls.

Prefer least privilege and explicit safeguards.
