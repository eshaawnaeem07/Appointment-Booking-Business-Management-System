from pydantic import BaseModel
from datetime import datetime
from app.utils.enums import AppointmentStatus


class AppointmentCreate(BaseModel):
    service_id: int
    start_time: datetime


class AppointmentOut(BaseModel):
    id: int
    user_id: int
    business_id: int
    service_id: int

    start_time: datetime
    end_time: datetime

    status: AppointmentStatus

    class Config:
        from_attributes = True