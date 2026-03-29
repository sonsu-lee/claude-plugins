# Research Plugin

Systematic technical research plugin for Claude Code with citation verification, source quality evaluation, and harness-based quality assurance.

## Features

- **7-step research workflow**: Protocol → Collection → Evaluation → Correction → Synthesis → Verification → Documentation
- **3 research modes**: Compare (A vs B), Validate (best practices check), Explore (deep dive)
- **Citation verification**: Every claim tracked with direct quotes and source URLs (MISSING_URL flagged as critical)
- **CRAAP+ source evaluation**: Automated quality scoring with lateral verification
- **Harness pattern**: Independent evaluator verifies synthesis quality with retry loops
- **403 fallback strategy**: WebFetch -> Exa crawling -> Zyte for anti-bot protected sites
- **PRISMA flow tracking**: Transparent source selection process
- **GRADE evidence ratings**: Confidence levels on every conclusion

## Setup

### Required: Exa API Key

1. Sign up at [exa.ai](https://exa.ai) and get an API key
2. Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export EXA_API_KEY="your-exa-api-key"
```

### Optional: Zyte API Key (for fallback)

Only needed when Exa/WebFetch cannot access a site (e.g., anti-bot protection):

```bash
export ZYTE_API_KEY="your-zyte-api-key"
```

### Install Plugin

```bash
# From the claude-plugins marketplace
claude plugin install ~/dev/personal/claude-plugins/research
```

## Usage

```
/research "Next.js vs Remix for a new e-commerce project"
/research "Is my React modal implementation following WAI-ARIA best practices?"
/research "How do React Server Components work under the hood?"
```

## Workflow

```
[1] Protocol Setup        → Define questions, criteria, dimensions
[2] Source Collection      → ctx7, Exa, WebFetch, Zyte
[3] Quality Evaluation     → CRAAP+ scoring, SIFT verification
[4] Coverage Correction    → Auto-expand search if gaps found
[5] Synthesis Analysis     → Thematic/Framework/Gap analysis
[6] Harness Verification   → Groundedness + Logic + Completeness
    ↳ FAIL → retry [5] or [2]
[7] Document Generation    → GRADE ratings, PRISMA flow, Evidence Gap Map
```

## Output

Research results are saved as markdown documents:
`research-YYYY-MM-DD-<topic-slug>.md`

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `EXA_API_KEY` | Yes | Exa semantic search API key |
| `ZYTE_API_KEY` | No | Zyte web scraping API key (fallback) |
