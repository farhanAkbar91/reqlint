from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "reqlint_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "cleanup-temp-files-every-15-mins": {
            "task": "app.workers.tasks.cleanup_temp_files",
            "schedule": 900.0,  # 15 minutes
        },
    }
)
