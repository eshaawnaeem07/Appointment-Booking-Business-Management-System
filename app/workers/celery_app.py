from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "bookingSystem",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.workers.tasks"],  # Explicitly include tasks
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,  # Acknowledge after task completes
    worker_prefetch_multiplier=1,  # Fetch one task at a time
)

# Backward-compatible name for Docker Compose or older commands that use
# app.workers.celery_app.celery.
celery = celery_app
