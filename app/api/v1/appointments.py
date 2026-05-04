from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.appointment import AppointmentCreate, AppointmentOut
from app.db.session import get_db
from app.services.appointment_services import AppointmentService
from app.core.dependencies import get_current_user

router = APIRouter(tags=["Appointments"])

@router.get("/appointments", response_model=list[AppointmentOut])
def get_my_appointments(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        return AppointmentService.get_my_appointments(db, user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch appointments: {str(e)}"
        )

@router.get("/appointments/{id}", response_model=AppointmentOut)
def get_appointment(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return AppointmentService.get_by_id(db, id, user)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch appointment: {str(e)}"
        )

@router.post(
    "/appointments",
    response_model=AppointmentOut,
    status_code=status.HTTP_201_CREATED
)
def book_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    try:
        return AppointmentService.book_appointment(db, user, payload)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to book appointment: {str(e)}"
        )

