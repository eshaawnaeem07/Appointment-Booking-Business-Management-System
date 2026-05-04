from pydantic import BaseModel, field_validator
from typing import Optional, List
from uuid import UUID
from app.utils.enums import DayEnum

# SINGLE HOUR SCHEMA
class BusinessHourBase(BaseModel):
    day_of_week: DayEnum
    is_open: bool
    open_time: Optional[str] = None
    close_time: Optional[str] = None
    @field_validator("day_of_week", mode="before")
    @classmethod
    def normalize_day(cls, v):
        if isinstance(v, str):
            v = v.strip().lower()
            mapping = {
                "mon": "Monday",
                "monday": "Monday",
                "tue": "Tuesday",
                "tuesday": "Tuesday",
                "wed": "Wednesday",
                "wednesday": "Wednesday",
                "thu": "Thursday",
                "thursday": "Thursday",
                "fri": "Friday",
                "friday": "Friday",
                "sat": "Saturday",
                "saturday": "Saturday",
                "sun": "Sunday",
                "sunday": "Sunday",
            }
            if v in mapping:
                return mapping[v]
        return v

    # @field_validator("open_time", "close_time")
    # @classmethod
    # def normalize_time(cls, v):
    #     if v is None:
    #         return v

    #     v = str(v)

    #     if v.isdigit():
    #         return f"{int(v):02d}:00:00"

    #     parts = v.split(":")
    #     if len(parts) == 2:
    #         return f"{v}:00"

    #     return v
    @field_validator("open_time", "close_time")
    @classmethod
    def normalize_time(cls, v):
        if v is None:
            return v

        v = str(v)

        if v.isdigit():
            return f"{int(v):02d}:00:00"

        parts = v.split(":")
        if len(parts) == 2:
            return f"{v}:00"

        if len(parts) == 3:
            return v

        raise ValueError("Invalid time format")


# CREATE 
class BusinessHourCreate(BusinessHourBase):
    pass

# UPDATE
class BusinessHourUpdate(BaseModel):
    day_of_week: Optional[DayEnum] = None
    is_open: Optional[bool] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None

# RESPONSE
class BusinessHourOut(BaseModel):
    id: UUID
    business_id: UUID
    day_of_week: DayEnum # want to see "Monday" in JSON
    is_open: bool
    open_time: Optional[str] 
    close_time: Optional[str]

    class Config:
        from_attributes = True 