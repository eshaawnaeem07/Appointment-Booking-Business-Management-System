from pydantic import BaseModel
from datetime import time


class BusinessHoursBase(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time
    is_closed: bool = False


class BusinessHoursCreate(BusinessHoursBase):
    pass


class BusinessHoursUpdate(BaseModel):
    start_time: time | None = None
    end_time: time | None = None
    is_closed: bool | None = None


class BusinessHoursOut(BusinessHoursBase):
    id: int

    class Config:
        from_attributes = True