from fastapi import HTTPException
from app.models.business_customer import BusinessCustomer
from app.models.business import Business

def get_customer_or_404(db, business_id, customer_id, user):
    customer = db.query(BusinessCustomer).join(Business).filter(
        BusinessCustomer.id == customer_id,
        BusinessCustomer.business_id == business_id,
        Business.owner_id == user.id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer