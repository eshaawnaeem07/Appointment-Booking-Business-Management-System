from app.workers.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.appointment import Appointment
from app.utils.enums import AppointmentStatus
from uuid import UUID


@celery_app.task(bind=True, name='app.workers.tasks.mark_no_show')
def mark_no_show(self, appointment_id: str):
    """Mark appointment as no_show if not confirmed within 4 hours"""
    print(f"[TASK STARTED] mark_no_show for appointment {appointment_id}")
    db = SessionLocal()

    try:
        # Convert string back to UUID
        appointment = db.query(Appointment).filter(
            Appointment.id == UUID(appointment_id)
        ).first()

        if appointment and appointment.status == AppointmentStatus.PENDING.value:
            appointment.status = AppointmentStatus.NO_SHOW.value
            db.commit()
            print(f"[✓ TASK SUCCESS] Appointment {appointment_id} marked as NO_SHOW")
            return {"status": "success", "appointment_id": appointment_id}
        else:
            print(f"[! TASK SKIPPED] Appointment {appointment_id} not found or already processed")
            return {"status": "skipped", "appointment_id": appointment_id}
    except Exception as e:
        print(f"[✗ TASK ERROR] Error marking appointment as no-show: {type(e).__name__}: {e}")
        # Don't raise - task completed but with info
        return {"status": "error", "appointment_id": appointment_id, "error": str(e)}
    finally:
        db.close()

