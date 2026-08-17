from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ReqLint FastAPI Backend",
        "nlp_engine": "Bilingual (ID/EN) Ready"
    }
