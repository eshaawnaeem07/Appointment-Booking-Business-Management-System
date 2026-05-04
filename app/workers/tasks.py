from app.workers.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.appointment import Appointment
from app.utils.enums import AppointmentStatus


@celery_app.task(bind=True)
def mark_no_show(self, appointment_id: int):
    print(f"[TASK STARTED] mark_no_show for appointment {appointment_id}")
    db = SessionLocal()

    try:
        appointment = db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()

        if appointment and appointment.status == AppointmentStatus.PENDING.value:
            appointment.status = AppointmentStatus.NO_SHOW.value
            db.commit()
    finally:
        db.close()

# @celery_app.task
# def test_task():
#     print("Task is working!")
