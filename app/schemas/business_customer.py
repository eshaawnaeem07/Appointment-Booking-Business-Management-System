from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class CustomerBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=10, max_length=15)
    email: EmailStr | None = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None

class CustomerOut(CustomerBase):
    id: UUID
    business_id: UUID
    user_id: UUID | None = None
    created_at: datetime

    class Config:
        from_attributes = True
