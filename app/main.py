from fastapi import FastAPI
from app.api.v1 import business
from app.api.v1.auth import router as auth_router
from app.db.base import Base
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware
from app.models import user, business, appointment, business_hours, payment, service
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(business.router)

@app.get("/")
def health():
    return {"status": "running"}
