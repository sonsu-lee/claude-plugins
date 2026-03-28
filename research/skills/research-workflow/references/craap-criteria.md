# CRAAP+ Source Quality Evaluation Framework

Adapted from the CRAAP Test (Currency, Relevance, Authority, Accuracy, Purpose) with an additional Version Alignment dimension for technical documentation.

## Scoring: 1-5 per dimension

### Currency (최신성)

| Score | Criteria |
|-------|----------|
| 5 | Published/updated within last 6 months, matches current stable version |
| 4 | Published/updated within last 1 year, matches recent version |
| 3 | Published/updated within last 2 years, may be slightly outdated |
| 2 | Published/updated 2-4 years ago, likely contains outdated information |
| 1 | Published 4+ years ago or date unknown |

### Relevance (관련성)

| Score | Criteria |
|-------|----------|
| 5 | Directly addresses the research question with specific technical detail |
| 4 | Closely related, provides substantial relevant information |
| 3 | Partially relevant, requires filtering to extract useful information |
| 2 | Tangentially related, limited useful information |
| 1 | Barely relevant to the research question |

### Authority (권위)

| Score | Criteria |
|-------|----------|
| 5 | Official documentation, RFC, or specification |
| 4 | Core maintainer/contributor blog, official tutorials |
| 3 | Well-known technical blog, reputable publication (e.g., Smashing Magazine) |
| 2 | Community blog with technical depth, Stack Overflow accepted answer |
| 1 | Personal blog, forum post, or unverified source |

### Accuracy (정확성)

| Score | Criteria |
|-------|----------|
| 5 | Verified by cross-referencing with 2+ other HIGH authority sources |
| 4 | Consistent with at least 1 other HIGH authority source |
| 3 | Appears accurate but not cross-verified |
| 2 | Contains some inaccuracies or unverified claims |
| 1 | Contains known inaccuracies or contradicts official sources |

### Version Alignment (버전 일치)

| Score | Criteria |
|-------|----------|
| 5 | Explicitly targets the exact version being researched |
| 4 | Targets the same major version |
| 3 | Targets a compatible version (minor differences unlikely to matter) |
| 2 | Targets a different major version but some info still applicable |
| 1 | Targets a completely different version or version not specified |

## Overall Rating

Calculate the average score across all 5 dimensions:

| Average | Rating |
|---------|--------|
| 4.0 - 5.0 | **HIGH** — Reliable, include in synthesis |
| 3.0 - 3.9 | **MEDIUM** — Usable with caveats, note limitations |
| 2.0 - 2.9 | **LOW** — Exclude from synthesis, document reason |
| 1.0 - 1.9 | **VERY LOW** — Discard |

## SIFT Lateral Verification

For Accuracy scoring, apply the SIFT method:

1. **Stop**: Don't immediately trust or dismiss the source
2. **Investigate the source**: Who wrote it? What's their expertise?
3. **Find better coverage**: What do OTHER sources say about this claim?
4. **Trace claims**: Can you find the original source of the claim?

Cross-reference key claims with at least one other independent source before rating Accuracy as 4 or 5.
