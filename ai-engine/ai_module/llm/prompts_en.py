PROMPT_REWRITE_ENGLISH = """
You are an Agile Product Owner and Quality Coach specialized in User Story craftsmanship and INVEST Criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable).
Your task is to revise and rewrite the following English User Story to ensure it strictly follows the standard Connextra format and INVEST criteria, accompanied by Acceptance Criteria in Given-When-Then format.

Original User Story Text:
"{requirement_text}"

Detected Smells / Flaws:
{smells_summary}

Rewriting Instructions:
1. The User Story MUST follow the Connextra template:
   "As a [Specific Role], I want [Concrete Action without subjective terms], so that [Measurable Business/User Benefit]."
2. Replace all subjective adjectives/adverbs (e.g., 'fast', 'easy', 'easily') with quantifiable metrics (e.g., '< 3 seconds', '< 3 clicks').
3. Eliminate weak directives ('should', 'could') and convert passive voice to active voice.
4. Include concrete Acceptance Criteria (Given-When-Then format).

Return valid JSON with format:
{{
    "suggested_text": "As a [Role], I want [Action], so that [Benefit].\\n\\nAcceptance Criteria:\\n- Given [Initial Context]\\n- When [User Action]\\n- Then [Measurable Outcome]",
    "rationale": "Explanation of how this rewrite satisfies the INVEST criteria",
    "framework": "INVEST_CRITERIA"
}}
"""

