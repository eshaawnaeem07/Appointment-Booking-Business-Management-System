uvicorn app.main:app --reload
1. Start Redis
redis-server
2. Start Celery Worker
celery -A app.workers.celery_app worker --loglevel=info

celery -A app.workers.celery_app worker --loglevel=info --pool=threads
3. Run FastAPI
uvicorn app.main:app --reload


celery -A app.workers.celery_app.celery flower --port=5555
