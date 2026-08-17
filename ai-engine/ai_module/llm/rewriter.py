import os
import json
from typing import List, Optional
from ..schemas.audit_models import SmellResult, RevisionSuggestion, LanguageCode
from .prompts_id import PROMPT_REWRITE_INDONESIAN
from .prompts_en import PROMPT_REWRITE_ENGLISH

class RequirementRewriter:
    """
    SLM / LLM Rewriter using Groq / LLaMA-3 / LangChain for Actionable SRS Revisions.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

    def generate_revision(
        self, text: str, smells: List[SmellResult], language: LanguageCode
    ) -> Optional[RevisionSuggestion]:
        if not smells:
            return None

        smells_summary = "\n".join([f"- [{s.category}] {s.message}" for s in smells])
        
        if language == LanguageCode.INDONESIAN:
            prompt = PROMPT_REWRITE_INDONESIAN.format(
                requirement_text=text,
                smells_summary=smells_summary
            )
        else:
            prompt = PROMPT_REWRITE_ENGLISH.format(
                requirement_text=text,
                smells_summary=smells_summary
            )

        # Fallback template if no API key is provided
        if not self.api_key:
            if language == LanguageCode.INDONESIAN:
                return RevisionSuggestion(
                    original_text=text,
                    suggested_text=f"Sistem HARUS {text.lower().replace('sebaiknya', '').replace('dapat', '')} dengan waktu respon < 200ms.",
                    rationale="Diubah dari direktif lemah menjadi 'HARUS' dengan kriteria kuantitatif terukur.",
                    framework="IEEE_29148"
                )
            else:
                return RevisionSuggestion(
                    original_text=text,
                    suggested_text=f"The system SHALL {text.lower().replace('should', '').replace('could', '')} within a response time < 200ms.",
                    rationale="Converted weak directive to explicit 'SHALL' with measurable quantitative threshold.",
                    framework="IEEE_29148"
                )

        try:
            # Groq / LangChain integration point
            from langchain_groq import ChatGroq
            llm = ChatGroq(groq_api_key=self.api_key, model_name="llama3-8b-8192")
            response = llm.invoke(prompt)
            data = json.loads(response.content)
            return RevisionSuggestion(
                original_text=text,
                suggested_text=data.get("suggested_text", text),
                rationale=data.get("rationale", "AI generated revision"),
                framework=data.get("framework", "IEEE_29148")
            )
        except Exception as e:
            # Soft fallback in case LLM API call fails
            return RevisionSuggestion(
                original_text=text,
                suggested_text=f"[Suggested] {text}",
                rationale=f"Automatic revision generated (LLM API offline: {str(e)})",
                framework="IEEE_29148"
            )
