---
name: en-polish
description: >
  This skill should be used when the user asks to "polish English text",
  "proofread my English", "rephrase in English", "fix my English", "make this
  sound natural", or needs English polishing for GitHub issues, PR descriptions,
  code reviews, Slack messages, emails, or technical documents. Also activated
  when any command references "en-polish skill".
---

# English Polishing for Professional Technical Communication

Make the text sound like it was written by a native English-speaking engineer,
calibrated to the right register for its platform.

## Non-Native Pattern Detection

Before any other pass, scan for Korean/Japanese L1 interference patterns:

- Missing or wrong articles (a/an/the) — Korean and Japanese have no articles
- Preposition errors mapped from particles ("discuss about", "explain about")
- Unnecessary hedging from Korean politeness ("I think maybe it might be...")
- Redundant subject repetition from topic-prominent structure
- Direct translation of Korean connectors ("Also additionally furthermore...")
- Passive where English prefers active ("It was decided by me to...")
- Missing subjects — Korean/Japanese often drop them; English rarely does
- Over-plural or under-plural based on mass noun patterns

See `references/non-native-patterns.md` for full detection list with examples.

## Multi-Pass Workflow

### Pass 1: Clarity

Remove noise. Every sentence should carry information.

- Strip filler openers ("Just wanted to", "Hope this finds you", "I was wondering if")
- Remove hedging that adds no meaning ("I think", "maybe", "kind of", "sort of")
  Exception: preserve where uncertainty is genuinely intended
- Merge redundant sentences
- Replace vague nouns with specific ones

### Pass 2: Naturalness

Make it sound like a native speaker wrote it.

- Fix article usage (a/an/the/zero article)
- Fix preposition collocations
- Vary sentence length
- Replace direct translations with natural English idioms
- Apply non-native pattern fixes from references/non-native-patterns.md

### Pass 3: Register Calibration

Calibrate to the platform context provided by the command.

- Apply the register table from `references/register-guide.md`
- Apply any hard rules specified by the command
- Check formality consistency throughout

See `references/register-guide.md` for platform register calibration and GitHub-specific conventions.

## Output Format

1. The polished text, ready to paste
2. Brief note (1-3 lines) on main changes — only if changes were significant

Skip the note for trivial fixes. Do not explain the skill or its process.
