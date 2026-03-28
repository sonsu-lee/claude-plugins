# Research Synthesis Methods Guide

This guide defines the synthesis methodologies used in each research mode.

## Thematic Synthesis (explore mode)

Based on Thomas & Harden (2008) three-stage approach:

### Stage 1: Line-by-line Extraction
- Extract specific claims, facts, and findings from each source
- Preserve original wording as direct quotes where possible
- Tag each extraction with source reference `[^N]`

### Stage 2: Descriptive Theme Grouping
- Group related extractions into descriptive themes
- Themes should emerge from the data, not be predetermined
- Each theme captures a distinct technical concept or pattern
- Example themes: "rendering strategy", "state management approach", "bundle optimization"

### Stage 3: Analytical Theme Generation
- Go beyond description to generate analytical insights
- Identify **mental models** — core conceptual frameworks that explain the technology
- Look for relationships between descriptive themes
- Generate insights that weren't explicitly stated in any single source but emerge from the synthesis

## Framework Synthesis (compare mode)

Based on Carroll et al. (2011) structured comparison approach:

### Step 1: Define Comparison Framework
- Use dimensions from the research protocol (Step 1)
- Common dimensions for technical comparison:
  - **Performance**: Runtime speed, bundle size, memory usage
  - **Developer Experience**: API design, tooling, debugging
  - **Ecosystem**: Community size, packages, integrations
  - **Learning Curve**: Documentation quality, concepts to learn
  - **Maturity**: Stability, production readiness, corporate backing
  - **Migration Path**: Adoption effort, breaking changes

### Step 2: Map Evidence to Framework
- For each dimension, extract relevant evidence from ALL compared technologies
- Each cell in the comparison table must have at least one citation
- If no evidence exists for a dimension, mark as "No evidence found"

### Step 3: Identify Consensus and Divergence
- **Consensus**: Sources agree on the relative comparison (e.g., "A is faster than B")
- **Divergence**: Sources disagree on the comparison or ranking
- For each divergence, proceed to meta-narrative analysis

## Gap Analysis (validate mode)

### Step 1: Map Current Implementation
- Document the user's current approach/pattern
- Identify specific technical decisions being validated

### Step 2: Collect Recommended Patterns
- Extract recommended/best practices from collected sources
- Focus on official documentation and authoritative guides

### Step 3: Analyze Gaps
For each difference between current and recommended:
- **Impact Level**: Critical / Important / Minor / Cosmetic
- **Evidence Strength**: Based on number and quality of sources
- **Migration Effort**: Estimated effort to align with recommendation
- **Risk of Not Changing**: Potential consequences

## Meta-narrative Analysis (all modes)

When sources disagree, apply meta-narrative thinking (Greenhalgh et al., 2005):

### Why Sources Disagree
Common reasons for divergence in technical documentation:

1. **Different Contexts**: Source A discusses large-scale apps, Source B discusses small projects
2. **Different Optimization Targets**: Source A optimizes for performance, Source B for DX
3. **Different Assumptions**: Source A assumes TypeScript, Source B assumes JavaScript
4. **Temporal Differences**: Source A was written before a major update
5. **Different Audiences**: Source A targets beginners, Source B targets experts
6. **Philosophical Differences**: Different schools of thought (e.g., OOP vs FP)

### How to Analyze
For each divergence point:
1. Identify WHAT specifically they disagree about
2. Identify WHO is making each claim (authority check)
3. Identify WHEN each claim was made (currency check)
4. Identify WHY they might disagree (context/assumption analysis)
5. Present the structural reason, not just the disagreement

## GRADE Evidence Rating

Apply GRADE-inspired confidence ratings to each key conclusion:

| Rating | Criteria |
|--------|----------|
| **HIGH** | Supported by 2+ HIGH-quality sources with direct evidence, no contradictions |
| **MODERATE** | Supported by 1 HIGH or 2+ MEDIUM sources, minor inconsistencies |
| **LOW** | Supported only by MEDIUM sources, or HIGH sources with indirect evidence |
| **VERY LOW** | Based primarily on inference, single LOW source, or significant contradictions |

Downgrade by one level if:
- Evidence is indirect (not directly addressing the question)
- Sources have conflicting findings
- Only a single source supports the conclusion

Upgrade by one level if:
- Multiple independent sources confirm the same finding
- Evidence comes from official specification/documentation
