from pydantic import BaseModel
from datetime import datetime

class BusinessCreate(BaseModel):
    name: str
    description: str | None = None

class BusinessUpdate(BaseModel):
    name: str | None = None 
    description: str | None = None

class BusinessResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True 