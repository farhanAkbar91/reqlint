PROMPT_REWRITE_ENGLISH = """
You are a Software Requirement Engineering Expert specializing in ISO/IEC/IEEE 29148 standards and INVEST criteria.
Your task is to rewrite the following English software requirement (SRS / User Story) to make it unambiguous, verifiable, and complete.

Original Requirement Text:
"{requirement_text}"

Detected Smells / Flaws:
{smells_summary}

Rewriting Instructions:
1. Use imperative directives ('shall' or 'must').
2. Convert passive voice to active voice identifying explicit actors/system.
3. Replace subjective adjectives (e.g., 'fast', 'user-friendly') with quantitative, measurable criteria.
4. Include Acceptance Criteria (Given-When-Then format) if applicable.

Return valid JSON with format:
{{
    "suggested_text": "...",
    "rationale": "...",
    "framework": "IEEE_29148"
}}
"""
