from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class BusinessHours(Base):
    __tablename__ = "business_hours"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)

    day_of_week = Column(Integer, nullable=False)  # 0=Mon, 6=Sun
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    is_open = Column(Boolean, default=False)

    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)

    business = relationship("Business", back_populates="hours")
