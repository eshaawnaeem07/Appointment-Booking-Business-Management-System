from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def health():
    return {"status": "running"}