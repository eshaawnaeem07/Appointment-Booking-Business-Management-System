from datetime import timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from app.models.business import Business
from app.models.service import Service
from app.utils.appointment_utils import (
    ensure_appointment_not_completed,
    ensure_appointment_owner,
    ensure_appointment_status,
    ensure_business_is_open,
    ensure_can_view_appointment,
    ensure_slot_available,
    ensure_user_owns_appointment,
    get_appointment_or_404,
    is_business_owner,ensure_future_appointment)
from app.utils.enums import AppointmentStatus
from app.workers.tasks import mark_no_show
from app.utils.customer_utils import get_customer_or_404


class AppointmentService:
    @staticmethod
    def get_my_appointments(db: Session, user):
        try:
            if is_business_owner(user):
                return db.query(Appointment).join(Service).join(Business).filter(
                    Business.owner_id == user.id
                ).all()

            return db.query(Appointment).filter(
                Appointment.user_id == user.id
            ).all()

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(500, "Failed to fetch appointments")

    @staticmethod
    def get_by_id(db: Session, appointment_id, user):
        try:
            appointment = get_appointment_or_404(db, appointment_id)
            ensure_can_view_appointment(appointment, user)
            return appointment

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(500, "Failed to fetch appointment")

    @staticmethod
    def book_appointment(db: Session, user, payload):
        try:
            service = db.query(Service).filter(
                Service.id == payload.service_id,
                Service.is_active == True
            ).first()

            if not service:
                raise HTTPException(404, "Service not found")

            if service.business.is_deleted:
                raise HTTPException(404, "Business not found")

            # (future-safe check)
            if payload.walk_in_customer_id and user.id:
                pass

            walk_in_customer_id = None

            if payload.walk_in_customer_id:
                customer = get_customer_or_404(
                    db,
                    service.business_id,
                    payload.walk_in_customer_id,
                    user
                )
                walk_in_customer_id = customer.id


            start_time = payload.start_time
            end_time = start_time + timedelta(minutes=service.duration)

            ensure_future_appointment(start_time)

            ensure_business_is_open(db, service, start_time, end_time)
            ensure_slot_available(db, service, start_time, end_time)

            user_id = user.id
            walk_in_customer = None

            if payload.walk_in_customer_id:
                user_id = None
                walk_in_customer = walk_in_customer_id

            appointment = Appointment(
                user_id=user_id,
                walk_in_customer_id=walk_in_customer, 
                business_id=service.business_id,
                service_id=service.id,
                start_time=start_time,
                end_time=end_time,
                status=AppointmentStatus.PENDING.value,
            )

            db.add(appointment)
            db.commit()
            db.refresh(appointment)
            try:
                if not service.requires_deposit:
                    mark_no_show.apply_async(
                        args=[appointment.id],
                        countdown=4 * 60 * 60,
                    )
            except Exception as e:
                print(f"Failed to schedule no-show task: {e}")

            return appointment

        except HTTPException:
            db.rollback()
            raise
        except Exception:
            db.rollback()
            raise HTTPException(500, "Failed to book appointment")
    
    @staticmethod
    def update_appointment(db: Session, appointment_id, user, payload):
        try:
            appointment = get_appointment_or_404(db, appointment_id)

            # Ensure user owns appointment
            ensure_user_owns_appointment(appointment, user)

            # Prevent updating completed appointments
            ensure_appointment_not_completed(appointment)

            service = appointment.service

            new_start_time = payload.start_time
            new_end_time = new_start_time + timedelta(minutes=service.duration)

            # Prevent past booking
            ensure_future_appointment(new_start_time)

            # Business hours validation
            ensure_business_is_open(
                db,
                service,
                new_start_time,
                new_end_time
            )

            # Check conflicting appointments
            conflict = db.query(Appointment).filter(
                Appointment.business_id == service.business_id,
                Appointment.id != appointment.id,
                Appointment.start_time < new_end_time,
                Appointment.end_time > new_start_time,
                Appointment.status.in_([
                    AppointmentStatus.PENDING.value,
                    AppointmentStatus.CONFIRMED.value,
                ])
            ).first()

            if conflict:
                raise HTTPException(400, "Time slot already booked")

            # Update appointment
            appointment.start_time = new_start_time
            appointment.end_time = new_end_time

            db.commit()
            db.refresh(appointment)

            return appointment

        except HTTPException:
            db.rollback()
            raise

        except Exception:
            db.rollback()
            raise HTTPException(500, "Failed to update appointment")
    @staticmethod
    def confirm_appointment(db: Session, appointment_id, user):
        try:
            appointment = get_appointment_or_404(db, appointment_id)
            ensure_user_owns_appointment(appointment, user)
            ensure_appointment_status(
                appointment,
                AppointmentStatus.PENDING,
                "Only pending appointments can be confirmed"
            )

            appointment.status = AppointmentStatus.CONFIRMED.value
            db.commit()
            db.refresh(appointment)
            return appointment

        except HTTPException:
            db.rollback()
            raise
        except Exception:
            db.rollback()
            raise HTTPException(500, "Failed to confirm appointment")

    @staticmethod
    def complete_appointment(db: Session, appointment_id, user):
        try:
            appointment = get_appointment_or_404(db, appointment_id)
            ensure_appointment_owner(appointment, user)
            ensure_appointment_status(
                appointment,
                AppointmentStatus.CONFIRMED,
                "Only confirmed appointments can be completed"
            )

            appointment.status = AppointmentStatus.COMPLETED.value
            db.commit()
            db.refresh(appointment)
            return appointment

        except HTTPException:
            db.rollback()
            raise
        except Exception:
            db.rollback()
            raise HTTPException(500, "Failed to complete appointment")

    @staticmethod
    def mark_no_show_manual(db: Session, appointment_id, user):
        try:
            appointment = get_appointment_or_404(db, appointment_id)
            ensure_appointment_owner(appointment, user)
            ensure_appointment_not_completed(appointment)

            appointment.status = AppointmentStatus.NO_SHOW.value
            db.commit()
            db.refresh(appointment)
            return appointment

        except HTTPException:
            db.rollback()
            raise
        except Exception:
            db.rollback()
            raise HTTPException(500, "Failed to mark appointment as no-show")

    @staticmethod
    def get_business_appointments(db: Session, business_id, user):
        try:
            business = db.query(Business).filter(
                Business.id == str(business_id),
                Business.owner_id == user.id
            ).first()

            if not business:
                raise HTTPException(403, "Not allowed")

            return db.query(Appointment).filter(
                Appointment.business_id == str(business_id)
            ).all()

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(500, "Failed to fetch business appointments")
