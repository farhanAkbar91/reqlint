from fastapi import APIRouter, Depends, status

from app.core.responses import success_response
from app.api.deps import get_current_user
from app.db.models import User
from app.schemas.audit import LintRequest
from app.services.nlp_stage1 import NLPStage1Service
from app.services.scoring import ScoringService

router = APIRouter(tags=["Lint"])

@router.post("/lint", status_code=status.HTTP_200_OK, summary="Real-time inline linting (stateless Stage 1)")
async def inline_lint(
    payload: LintRequest,
    current_user: User = Depends(get_current_user)
):
    raw_text = payload.konten.strip()
    if not raw_text:
        return success_response(
            message="OK",
            data={
                "skor_perkiraan": 100.0,
                "ringkasan": {
                    "ambiguity": 0,
                    "tidak_lengkap": 0,
                    "weak_directive": 0,
                    "passive_voice": 0,
                    "total": 0
                },
                "temuan": []
            }
        )

    stage1_res = NLPStage1Service.analyze_draft(raw_text)
    findings = stage1_res["findings"]
    stories = stage1_res["stories"]
    score_res = ScoringService.calculate_score(stories, findings)

    # Convert findings to clean response list
    lint_findings = [
        {
            "kategori_cacat": f["kategori_cacat"],
            "severity": f["severity"],
            "potongan_teks_asli": f["potongan_teks_asli"],
            "highlight_start": f["highlight_start"],
            "highlight_end": f["highlight_end"],
            "saran_perbaikan": f["saran_perbaikan"]
        }
        for f in findings
    ]

    return success_response(
        message="OK",
        data={
            "skor_perkiraan": score_res["skor_kualitas"],
            "ringkasan": stage1_res["ringkasan"],
            "temuan": lint_findings
        }
    )
