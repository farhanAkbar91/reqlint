import os
import re
import json
from typing import List, Optional
from ..schemas.audit_models import SmellResult, RevisionSuggestion, LanguageCode
from .prompts_id import PROMPT_REWRITE_INDONESIAN
from .prompts_en import PROMPT_REWRITE_ENGLISH

class RequirementRewriter:
    """
    SLM / LLM Rewriter using Groq / LLaMA-3 / LangChain for Actionable User Story Revisions.
    Transforms flawed user stories into INVEST-compliant stories with Acceptance Criteria.
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
                cleaned_text = text
                for w in ["sebaiknya", "dapat", "bisa", "mungkin", "diharapkan", "sekiranya"]:
                    cleaned_text = re.sub(rf'\b{w}\b', '', cleaned_text, flags=re.IGNORECASE)
                cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

                if not re.search(r'\bsebagai\b', cleaned_text, re.IGNORECASE):
                    cleaned_text = f"Sebagai Pengguna, saya ingin {cleaned_text}"
                if not re.search(r'\b(sehingga|agar|supaya)\b', cleaned_text, re.IGNORECASE):
                    cleaned_text = f"{cleaned_text}, sehingga aktivitas dapat diselesaikan dalam waktu < 3 detik."

                suggested = (
                    f"{cleaned_text}\n\n"
                    f"Kriteria Penerimaan (Acceptance Criteria):\n"
                    f"- Given pengguna telah masuk ke sistem\n"
                    f"- When pengguna menjalankan aksi yang diminta\n"
                    f"- Then sistem memproses dan merespons dalam waktu < 2 detik dengan status sukses."
                )
                return RevisionSuggestion(
                    original_text=text,
                    suggested_text=suggested,
                    rationale="Diformat ulang ke standar User Story Connextra (Role-Action-Benefit) & dilengkapi Kriteria Penerimaan (Given-When-Then) sesuai kriteria INVEST.",
                    framework="INVEST_CRITERIA"
                )
            else:
                cleaned_text = text
                for w in ["should", "could", "may", "might", "ought to"]:
                    cleaned_text = re.sub(rf'\b{w}\b', '', cleaned_text, flags=re.IGNORECASE)
                cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

                if not re.search(r'\bas an?\b', cleaned_text, re.IGNORECASE):
                    cleaned_text = f"As a User, I want to {cleaned_text}"
                if not re.search(r'\b(so that|in order to)\b', cleaned_text, re.IGNORECASE):
                    cleaned_text = f"{cleaned_text}, so that the action completes within < 3 steps."

                suggested = (
                    f"{cleaned_text}\n\n"
                    f"Acceptance Criteria:\n"
                    f"- Given the user is authenticated\n"
                    f"- When the user performs the requested action\n"
                    f"- Then the system processes the request in < 2 seconds and displays a success notification."
                )
                return RevisionSuggestion(
                    original_text=text,
                    suggested_text=suggested,
                    rationale="Reformatted to standard Connextra User Story format (Role-Action-Benefit) and added Given-When-Then Acceptance Criteria fulfilling INVEST.",
                    framework="INVEST_CRITERIA"
                )

        try:
            from langchain_groq import ChatGroq
            llm = ChatGroq(groq_api_key=self.api_key, model_name="llama3-8b-8192")
            response = llm.invoke(prompt)
            data = json.loads(response.content)
            return RevisionSuggestion(
                original_text=text,
                suggested_text=data.get("suggested_text", text),
                rationale=data.get("rationale", "AI generated INVEST revision"),
                framework=data.get("framework", "INVEST_CRITERIA")
            )
        except Exception as e:
            return RevisionSuggestion(
                original_text=text,
                suggested_text=f"[Suggested] {text}",
                rationale=f"Automatic revision generated (LLM API offline: {str(e)})",
                framework="INVEST_CRITERIA"
            )

