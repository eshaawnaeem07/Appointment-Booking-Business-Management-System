uvicorn app.main:app --reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
1. Start Redis
redis-server
2. Start Celery Worker
celery -A app.workers.celery_app worker --loglevel=info

celery -A app.workers.celery_app worker --loglevel=info --pool=threads
3. Run FastAPI
uvicorn app.main:app --reload


celery -A app.workers.celery_app.celery flower --port=5555

4. Stripe CLI
stripe login
stripe listen --forward-to localhost:8000/payments/webhook