---
name: research
description: Conduct systematic technical research with citation verification and quality assurance
argument-hint: "<research question or topic>"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Agent, mcp__plugin_research_exa__web_search_exa, mcp__plugin_research_exa__crawling_exa, mcp__plugin_research_exa__get_code_context_exa]
---

# /research Command

You have been asked to conduct systematic technical research on: **$ARGUMENTS**

## Instructions

1. Invoke the `research-workflow` skill to begin the 7-step research process.
2. The skill will guide you through: protocol setup → source collection → quality evaluation → coverage correction → synthesis → harness verification → document generation.
3. All outputs must follow the research output template in `references/output-template.md`.

Begin by activating the research-workflow skill now.
