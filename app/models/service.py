from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(String, ForeignKey("businesses.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String)

    duration = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    requires_deposit = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    business = relationship("Business", back_populates="services")
    appointments = relationship("Appointment", back_populates="service")