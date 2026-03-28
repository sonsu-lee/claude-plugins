---
name: research-workflow
description: >
  Use when the user asks to research a technical topic, compare libraries/frameworks,
  validate an implementation against best practices, or explore a technology in depth.
  Triggers on: /research command, "research this", "compare X vs Y", "is this the right approach",
  "what's the best practice for", "investigate", "deep dive into".
---

# Systematic Technical Research Workflow

You are conducting systematic technical research. Follow this 7-step process exactly.
Do NOT skip steps. Each step produces an output that feeds into the next.

## Research Modes

Determine the mode from the user's question:

- **compare**: Comparing two or more technologies/approaches (e.g., "Next.js vs Remix")
- **validate**: Checking if a current implementation follows best practices (e.g., "Is this modal pattern accessible?")
- **explore**: Deep investigation of a single topic (e.g., "How do React Server Components work?")

## Harness Loop Control

This workflow uses a harness pattern (generator/evaluator separation). Steps 2-6 form a loop:

- **Max synthesis retries**: 3 (Step 5 → Step 6 → back to Step 5)
- **Max collection retries**: 2 (Step 6 → back to Step 2)
- If max retries exceeded: proceed with best available results and note limitations in the final document

## Step 1: Protocol Setup

Launch the `research-planner` agent with the user's research question.

The agent will produce a **research protocol** containing:
- Refined core question and auto-generated sub-questions
- Research mode (compare/validate/explore)
- Inclusion/exclusion criteria (e.g., "official docs only", "v14+", "after 2024")
- Comparison dimensions (compare mode): performance, DX, ecosystem, learning curve, etc.
- Extraction targets: what to extract from each source

Present the protocol to the user for confirmation before proceeding. The protocol serves as the **sprint contract** — the evaluator (Step 6) will judge completeness against it.

## Step 2: Source Collection

Launch the `doc-researcher` agent with the approved protocol.

The agent will collect sources following this priority:
1. **ctx7** (official documentation) — run `npx ctx7@latest library` then `npx ctx7@latest docs`
2. **Exa MCP** (semantic search + original text extraction)
3. **WebFetch** (direct URL content extraction)
4. **Zyte** (fallback for anti-bot protected sites, requires ZYTE_API_KEY)

The agent MUST:
- Track PRISMA flow: Found(N) → Screened(M) → Excluded(with reasons) → Included(K)
- Attach **direct quotes** and **source URLs** to every piece of information
- Tag each item: `[VERIFIED]` (from source text) or `[INFERRED]` (reasoning/interpretation)
- Apply inclusion/exclusion criteria from the protocol

Output: Raw data per source + PRISMA flow record

## Step 3: Source Quality Evaluation

Launch the `source-evaluator` agent with the collected sources.

The agent evaluates each source using the CRAAP+ framework (see `references/craap-criteria.md`):
- **Currency**: Publication/update date, technology version alignment
- **Relevance**: Direct relevance to the research question
- **Authority**: Official docs > core contributors > blogs > personal opinions
- **Accuracy**: Cross-verification with other sources (lateral verification via SIFT method)
- **Version Alignment**: Does the source match the target version being researched?

Each source receives a score (1-5 per dimension) and an overall rating: HIGH / MEDIUM / LOW.
Sources scoring LOW are excluded with documented reasons.

Output: Quality scores per source + excluded sources with reasons

## Step 4: Coverage Correction (CRAG)

Evaluate collection sufficiency against the protocol:

- Check: Does every sub-question have at least 2 HIGH-quality sources?
- Check: Are all comparison dimensions (compare mode) covered?
- Check: Are all extraction targets addressed?

If insufficient:
1. Identify specific gaps
2. Generate expanded/modified search queries targeting the gaps
3. Re-run Step 2 (doc-researcher) for the gaps only
4. Re-run Step 3 (source-evaluator) for new sources
5. Repeat up to **2 times** maximum

If still insufficient after retries: document the gaps explicitly and proceed.

## Step 5: Synthesis Analysis

Launch the `research-synthesizer` agent with evaluated sources.

Apply mode-specific synthesis methodology (see `references/synthesis-methods.md`):

### explore mode → Thematic Synthesis
1. Line-by-line extraction from source texts
2. Descriptive theme grouping (technical themes)
3. Analytical theme generation → derive mental models

### compare mode → Framework Synthesis
1. Map evidence to predefined comparison dimensions from the protocol
2. Build systematic comparison table per dimension
3. Identify consensus points and divergence points per dimension

### validate mode → Gap Analysis
1. Map current implementation against recommended patterns
2. Analyze each gap's rationale and impact level

### All modes — Meta-narrative Analysis
For every divergence point:
- Do NOT just list "A says X, B says Y"
- Explain WHY they disagree: different contexts, assumptions, optimization targets
- Provide structural analysis of the disagreement

The synthesizer MUST:
- Base all conclusions on collected evidence only (minimize new inference)
- Use footnote format `[^N]` linking to specific source passages
- Explicitly mark areas with insufficient evidence

Output: Synthesis results (themes, comparison tables, consensus/divergence, meta-narratives)

## Step 6: Harness Verification

Launch the `research-evaluator` agent with the synthesis results AND the original protocol.

The evaluator performs three checks:

### A. Groundedness Verification
- Match each claim to its cited source passage
- Detect post-rationalization (claim cites a source but the source doesn't contain that information)
- Flag ungrounded claims as `[UNVERIFIED]`

### B. Logical Validity
- Verify conclusions follow logically from evidence
- Detect logical leaps or over-generalizations
- Verify meta-narratives reflect actual contextual differences

### C. Protocol Completeness (Sprint Contract)
- All sub-questions from Step 1 answered?
- All comparison dimensions covered (compare mode)?
- Minimum source threshold met?
- Extraction targets addressed?

### Evaluation Result
- **PASS**: Proceed to Step 7
- **FAIL — Source Gap**: Return to Step 2 with specific gap description (max 2 retries)
- **FAIL — Synthesis Error**: Return to Step 5 with specific issues to fix (max 3 retries)
- **FAIL — Groundedness**: Return to Step 5 to correct flagged claims (counts as synthesis retry)

If max retries exceeded: proceed with current best results, noting all unresolved issues.

## Step 7: Document Generation

Generate the final research document using the template in `references/output-template.md`.

The document MUST include:
- **GRADE evidence ratings**: HIGH/MODERATE/LOW/VERY LOW confidence per key conclusion
- **PRISMA flow summary**: "N found → M screened → K included"
- **Evidence Gap Map**: explicitly list areas where evidence was insufficient
- **Inline footnotes** with source spans (direct quotes from original text)
- **Research metrics**: total sources, average CRAAP score, groundedness pass rate, evidence grade distribution

Save the document to the current working directory as `research-YYYY-MM-DD-<topic-slug>.md`.

Inform the user that the research is complete and provide a brief summary of key findings.
