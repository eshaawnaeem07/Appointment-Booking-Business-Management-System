from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.v1.business import router as business_router
from app.api.v1.auth import router as auth_router
from app.api.v1.business_hours import router as business_hours_router
from app.api.v1.services import router as services_router
from app.api.v1.appointments import router as appointment_router
from app.api.v1.business_customers import router as customers_router

from app.db.base import Base
from app.db.session import engine

from app.models import user, business, appointment, business_hours, payment, service

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000,http://localhost:8080",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(business_router)
app.include_router(business_hours_router)
app.include_router(services_router)
app.include_router(appointment_router)
app.include_router(customers_router)

# @app.get("/")
# def health():
#     return {"status": "running"}

# @app.get("/test-task")
# def run_test_task():
#     task = test_task.delay()
#     return {
#         "message": "Task sent",
#         "task_id": task.id
#     }
@app.get("/test-task")
def test_task():
    from app.workers.tasks import mark_no_show

    mark_no_show.delay(1)
    return {"message": "Task sent"}
