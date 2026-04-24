from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import business as schema
from app.services import business_service as service
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/businesses", tags=["businesses"])

# GET ALL BUSINESSES (PUBLIC)
@router.get("/", response_model=list[schema.BusinessResponse])
def list_businesses(db: Session = Depends(get_db)):
    try:
        return service.get_all_businesses(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET BY ID (PUBLIC)
@router.get("/{business_id}", response_model=schema.BusinessResponse)
def get_business(business_id: int, db: Session = Depends(get_db)):
    try:
        business = service.get_business(db, business_id)
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        return business

    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CREATE BUSINESS (JWT + BUSINESS ROLE)
@router.post("/", response_model=schema.BusinessResponse)
def create_business(
    data: schema.BusinessCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        return service.create_business(db, data, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# UPDATE BUSINESS (OWNER ONLY)
@router.put("/{business_id}", response_model=schema.BusinessResponse)
def update_business(
    business_id: int,
    data: schema.BusinessUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        business = service.get_business(db, business_id)

        if not business:
            raise HTTPException(status_code=404, detail="Not found")

        if business.owner_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

        return service.update_business(db, business, data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE BUSINESS (OWNER ONLY)
@router.delete("/{business_id}")
def delete_business(
    business_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        business = service.get_business(db, business_id)
        if not business:
            raise HTTPException(status_code=404, detail="Not found")
        if business.owner_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")
        service.delete_business(db, business)
        return {"message": "Business deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

