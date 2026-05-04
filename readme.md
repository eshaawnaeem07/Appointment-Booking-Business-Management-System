uvicorn app.main:app --reload

1. Start Redis
redis-server
2. Start Celery Worker
celery -A app.workers.celery_app worker --loglevel=info
3. Run FastAPI
uvicorn app.main:app --reload


celery -A app.workers.celery_app.celery flower --port=5555

## Docker setup

This project now has Docker support for:

- FastAPI backend
- React/Vite frontend served by Nginx
- PostgreSQL
- Redis
- Celery worker
- Flower dashboard

### 1. Start Docker Desktop

Open Docker Desktop first and wait until it says Docker is running.

### 2. Optional email variables

For password reset emails, set these variables in your shell before running Compose:

```powershell
$env:DOCKER_SENDGRID_API_KEY="your-sendgrid-key"
$env:DOCKER_FROM_EMAIL="you@example.com"
```

If you skip this, the app still starts, but email sending will fail when that feature is used.

### 3. Build and start everything

```powershell
docker compose up --build
```

### 4. Open the apps

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs
- Flower: http://localhost:5555
- PostgreSQL on host: localhost:5400
- Redis on host: localhost:6379

### 5. Useful commands

```powershell
docker compose ps
docker compose logs api
docker compose logs celery
docker compose down
```

To delete database and Redis volumes too:

```powershell
docker compose down -v
```
