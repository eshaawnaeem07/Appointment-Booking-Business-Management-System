from pydantic import BaseModel


class ServiceBase(BaseModel):
    name: str
    description: str | None = None
    duration: int
    price: float
    requires_deposit: bool = False


class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    duration: int | None = None
    price: float | None = None
    requires_deposit: bool | None = None


class ServiceOut(ServiceBase):
    id: int

    class Config:
        from_attributes = True