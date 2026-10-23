import asyncio
import os
import time
import logging
from app.workers.celery_app import celery_app
from app.services.audit_service import AuditService
from app.core.config import settings

logger = logging.getLogger("reqlint.tasks")

@celery_app.task(name="app.workers.tasks.run_audit_task")
def run_audit_task(id_audit: int):
    logger.info(f"Running celery audit task for id_audit={id_audit}")
    asyncio.run(AuditService.run_pipeline(id_audit))

@celery_app.task(name="app.workers.tasks.cleanup_temp_files")
def cleanup_temp_files():
    temp_dir = settings.TEMP_DIR
    if not os.path.exists(temp_dir):
        return

    now = time.time()
    ttl_seconds = settings.TEMP_TTL_MINUTES * 60

    for fname in os.listdir(temp_dir):
        fpath = os.path.join(temp_dir, fname)
        if os.path.isfile(fpath):
            try:
                mtime = os.path.getmtime(fpath)
                if now - mtime > ttl_seconds:
                    os.remove(fpath)
                    logger.info(f"Cleaned up stale temp file: {fpath}")
            except Exception as e:
                logger.error(f"Failed to remove temp file {fpath}: {e}")
