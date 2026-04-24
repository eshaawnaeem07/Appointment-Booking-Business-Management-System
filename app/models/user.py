from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base
from app.utils.enums import UserRole
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default=UserRole.USER.value)
    reset_token = Column(String, nullable=True)
    token_expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    hours = relationship("BusinessHours", back_populates="business")
    services = relationship("Service", back_populates="business")
    appointments = relationship("Appointment", foreign_keys="Appointment.user_id", back_populates="user")
    business_appointments = relationship("Appointment", foreign_keys="Appointment.business_id", back_populates="business")
    businesses = relationship("Business", back_populates="owner")