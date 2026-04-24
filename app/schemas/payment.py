from pydantic import BaseModel
from app.utils.enums import PaymentStatus


class PaymentCreateSession(BaseModel):
    appointment_id: int


class PaymentOut(BaseModel):
    id: int
    appointment_id: int
    status: PaymentStatus

    class Config:
        from_attributes = True