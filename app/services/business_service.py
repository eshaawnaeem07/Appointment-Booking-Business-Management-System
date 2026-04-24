from sqlalchemy.orm import Session
from app.models.business import Business
from app.utils.enums import UserRole

# GET ALL
def get_all_businesses(db: Session):
    try:
        return db.query(Business).all()
    except Exception as e:
        raise Exception(f"Error fetching businesses: {str(e)}")

# CREATE BUSINESS
def create_business(db: Session, data, user):
    try:
        user_role = UserRole(user.role)
    except ValueError:
        raise Exception("Invalid user role")
    
    if user.role != UserRole.BUSINESS.value:
        raise Exception("Only business users can create business")

    business = Business(
        name=data.name,
        description=data.description,
        owner_id=user.id
    )
    db.add(business)
    db.commit()
    db.refresh(business)
    return business


# GET BY ID
def get_business(db: Session, business_id: int):
    try:
        return db.query(Business).filter(Business.id == business_id).first()
    except Exception as e:
        raise Exception(f"Error fetching business: {str(e)}")

# UPDATE
def update_business(db: Session, business, data):
    try:
        if data.name:
            business.name = data.name
        if data.description:
            business.description = data.description

        db.commit()
        db.refresh(business)
    except Exception as e:
        raise Exception(f"Error updating business: {str(e)}")
    return business

# DELETE
def delete_business(db: Session, business):
    try:
        db.delete(business)
        db.commit()
    except Exception as e:
        raise Exception(f"Error deleting business: {str(e)}")