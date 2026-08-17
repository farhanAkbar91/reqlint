"""
English Requirement Smell Dictionaries based on IEEE 29148 & INVEST
"""

ENGLISH_WEAK_DIRECTIVES = {
    "should": "Use imperative 'shall' or 'must' to specify mandatory system requirements.",
    "could": "Indicates optional capability. Clarify if this is a mandatory requirement.",
    "may": "Ambiguous permission vs obligation. Replace with explicit system behavior.",
    "might": "High uncertainty. Remove speculative language.",
    "ought to": "Non-binding language. Replace with 'shall'.",
    "etc": "Avoid open-ended lists. Enumerate all items explicitly.",
    "and so on": "Avoid open-ended qualifications. List all required options."
}

ENGLISH_SUBJECTIVE_ADJECTIVES = {
    "fast": "Specify measurable response time threshold (e.g., response time < 200 ms).",
    "easy": "Define concrete usability metric (e.g., completed within 3 clicks).",
    "easily": "Define concrete usability metric (e.g., completed within 3 clicks).",
    "reliable": "Specify SLA or availability target (e.g., 99.9% uptime).",
    "secure": "Specify exact security standard or encryption algorithm (e.g., TLS 1.3 / AES-256).",
    "user-friendly": "Define explicit UX acceptance criteria.",
    "efficient": "State measurable CPU, memory, or throughput limit.",
    "robust": "Define specific error handling and recovery expectations."
}

ENGLISH_VAGUE_QUANTIFIERS = {
    "some": "Specify exact quantity or precise numeric range.",
    "most": "State exact percentage or measurable quantitative target.",
    "many": "State explicit numeric limit.",
    "several": "Specify exact count.",
    "approximately": "Provide strict acceptable tolerance bounds."
}
