from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
from app.core.responses import success_response

router = APIRouter()

@router.get("/health", summary="Healthcheck")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "down"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "up"
    except Exception:
        db_status = "down"

    redis_status = "up"
    if settings.AUDIT_EXECUTION_MODE == "celery":
        try:
            import redis
            r = redis.from_url(settings.REDIS_URL)
            r.ping()
            redis_status = "up"
        except Exception:
            redis_status = "down"
    else:
        redis_status = "up"

    slm_status = "mock" if settings.SLM_PROVIDER == "mock" else "up"

    return success_response(
        message="OK",
        data={
            "db": db_status,
            "redis": redis_status,
            "slm": slm_status,
            "version": settings.VERSION
        }
    )
