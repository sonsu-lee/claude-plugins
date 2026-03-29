#!/usr/bin/env python3
"""
SubagentStop hook: Verify citations in research output.

Checks that the research synthesis output contains proper citation formatting,
source URLs, and minimum source requirements. This is a lightweight format check;
deep groundedness verification is handled by the research-evaluator agent.
"""

import json
import re
import sys


def verify_citations(text: str) -> dict:
    """Verify citation format and presence in the output text."""
    issues = []

    # Check for footnote references [^N]
    footnote_refs = set(re.findall(r'\[\^(\d+)\]', text))

    # Check for footnote definitions [^N]: ...
    footnote_defs = set(re.findall(r'^\[\^(\d+)\]:', text, re.MULTILINE))

    # Check for undefined references
    undefined = footnote_refs - footnote_defs
    if undefined:
        issues.append(
            f"Footnote references without definitions: {', '.join(f'[^{n}]' for n in sorted(undefined))}"
        )

    # Check for unreferenced definitions
    unreferenced = footnote_defs - footnote_refs
    if unreferenced:
        issues.append(
            f"Footnote definitions never referenced: {', '.join(f'[^{n}]' for n in sorted(unreferenced))}"
        )

    # Check minimum citation count
    if len(footnote_defs) < 3:
        issues.append(
            f"Only {len(footnote_defs)} sources cited. Minimum recommended: 3"
        )

    # Check for URL presence in footnote definitions
    url_pattern = re.compile(r'^\[\^\d+\]:.*https?://', re.MULTILINE)
    urls_in_footnotes = url_pattern.findall(text)
    if footnote_defs and len(urls_in_footnotes) < len(footnote_defs) * 0.8:
        issues.append(
            f"Only {len(urls_in_footnotes)}/{len(footnote_defs)} footnotes contain URLs"
        )

    # Check for direct quotes in footnotes (text in quotation marks)
    quote_pattern = re.compile(r'^\[\^\d+\]:.*["\u201c].*["\u201d]', re.MULTILINE)
    quotes_in_footnotes = quote_pattern.findall(text)
    if footnote_defs and len(quotes_in_footnotes) < len(footnote_defs) * 0.5:
        issues.append(
            f"Only {len(quotes_in_footnotes)}/{len(footnote_defs)} footnotes contain direct quotes. "
            "Research requires original text citations."
        )

    # Check for MISSING_URL flags from the research-evaluator
    missing_url_count = len(re.findall(r'MISSING_URL', text))
    if missing_url_count > 0:
        issues.append(
            f"{missing_url_count} MISSING_URL flag(s) detected. "
            "Every footnote must include a source URL for verification."
        )

    # Check for VERIFIED/INFERRED tags (in source collection output)
    verified_count = len(re.findall(r'\[VERIFIED\]', text))
    inferred_count = len(re.findall(r'\[INFERRED\]', text))
    if verified_count + inferred_count > 0 and inferred_count > verified_count:
        issues.append(
            f"More inferred ({inferred_count}) than verified ({verified_count}) claims. "
            "Research should be primarily evidence-based."
        )

    # Check for evidence grade tags
    grade_tags = re.findall(r'\[(HIGH|MODERATE|LOW|VERY LOW)\]', text)
    has_grade_section = 'Evidence Grade' in text or '증거 등급' in text

    # Check for PRISMA flow
    has_prisma = bool(
        re.search(r'PRISMA|found.*screened.*included|발견.*스크리닝.*포함', text, re.IGNORECASE)
    )

    return {
        "footnote_refs": len(footnote_refs),
        "footnote_defs": len(footnote_defs),
        "urls_found": len(urls_in_footnotes),
        "quotes_found": len(quotes_in_footnotes),
        "missing_url_flags": missing_url_count,
        "verified_claims": verified_count,
        "inferred_claims": inferred_count,
        "grade_tags": len(grade_tags),
        "has_prisma": has_prisma,
        "has_grades": has_grade_section or len(grade_tags) > 0,
        "issues": issues,
    }


def main():
    try:
        input_data = json.load(sys.stdin)
        agent_name = input_data.get("agent_name", "")
        output = input_data.get("output", "")

        if not output:
            result = {"decision": "allow"}
            print(json.dumps(result), file=sys.stdout)
            sys.exit(0)

        verification = verify_citations(output)

        if verification["issues"]:
            message_parts = ["[Research Citation Check]"]
            for issue in verification["issues"]:
                message_parts.append(f"  - {issue}")
            message_parts.append("")
            message_parts.append(
                "Please address these citation issues before finalizing the research document."
            )

            result = {
                "decision": "allow",
                "systemMessage": "\n".join(message_parts),
            }
        else:
            result = {"decision": "allow"}

        print(json.dumps(result), file=sys.stdout)

    except Exception as e:
        error_result = {
            "decision": "allow",
            "systemMessage": f"[Citation Hook] Warning: verification script error: {e}",
        }
        print(json.dumps(error_result), file=sys.stdout)

    finally:
        sys.exit(0)


if __name__ == "__main__":
    main()
