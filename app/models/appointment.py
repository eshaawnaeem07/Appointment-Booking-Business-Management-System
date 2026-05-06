from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.utils.enums import AppointmentStatus
from datetime import datetime


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    business_id = Column(String, ForeignKey("businesses.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    
    walk_in_customer_id = Column(Integer, ForeignKey("business_customers.id"), nullable=True)

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    status = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="appointments")
    business = relationship("Business", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")

    payment = relationship("Payment", back_populates="appointment", uselist=False)
    walk_in_customer = relationship("BusinessCustomer", back_populates="appointments")