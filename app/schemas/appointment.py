from pydantic import BaseModel
from datetime import datetime
from app.utils.enums import AppointmentStatus
from uuid import UUID

class AppointmentCreate(BaseModel):
    service_id: int
    start_time: datetime
    walk_in_customer_id: int | None = None
    


class AppointmentOut(BaseModel):
    id: int
    user_id: int | None = None
    business_id: UUID
    service_id: int

    start_time: datetime
    end_time: datetime

    status: AppointmentStatus
    walk_in_customer_id: int | None = None  

    class Config:
        from_attributes = True
