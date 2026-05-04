from app.workers.celery_app import celery
from app.db.session import SessionLocal
from app.models.appointment import Appointment
from app.utils.enums import AppointmentStatus


@celery.task
def mark_no_show(appointment_id: int):
    db = SessionLocal()

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if appointment and appointment.status == AppointmentStatus.PENDING.value:
        appointment.status = AppointmentStatus.NO_SHOW.value
        db.commit()

    db.close()
