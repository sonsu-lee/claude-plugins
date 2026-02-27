# Register Calibration Guide

## Platform Register Table

| Platform | Register | Key signals |
|---|---|---|
| GitHub Issue | Professional-technical | Direct, specific, no filler |
| GitHub PR | Professional-technical | Impersonal ("this PR"), imperative titles |
| GitHub Review | Professional-collegial | Collaborative, suggesting tone |
| Slack (channel) | Casual-professional | Contractions OK, brief, direct |
| Slack (thread) | Casual-professional | Even briefer, context-aware |
| Slack (DM) | Casual | Informal opener OK, shorter |
| Email (external) | Formal-professional | Full sentences, no contractions |
| Email (internal) | Professional | Between casual and formal |
| README | Instructional | Second-person "you", active |
| Tech doc | Instructional | Second-person, scannable |
| Changelog | Neutral-technical | Past tense, specific |
| Commit message | Neutral-technical | Imperative, no period |

## Common Non-Native Formality Mismatches

These patterns feel natural to Korean/Japanese speakers but land wrong in English:

- Starting GitHub comments with "Dear Sir/Madam" or "Hello" → drop the opener entirely
- Starting Slack with "I hope this message finds you well" → just say the thing
- Ending all messages with "Thank you for your consideration" → only in formal email
- Using "Please kindly" → "Please" is enough; "kindly" sounds stiff in tech

## GitHub-Specific Conventions

### Issue Titles
- Describe the problem, not the solution
- No trailing period. Under 72 chars when possible.

### PR Titles
- Imperative mood: "Add retry logic" not "Added retry logic"
- Max 72 chars. No "WIP:" unless actually draft.

### PR Body
- What: what changed. Why: motivation. How: approach (optional for simple PRs).
- No first-person "I" ("This PR adds..." not "I added...")
- No apology language ("Sorry this took so long")

### Code Review Comments
- Suggest, don't demand: "Consider extracting this..." not "Extract this"
- Explain why: "This will throw if X is null" not just "null check"
- Prefix with type when helpful: "nit:", "suggestion:", "question:"
