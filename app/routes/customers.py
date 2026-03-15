from fastapi import APIRouter, Depends, HTTPException
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

router = APIRouter()

def get_payment_service():
    repo = FakePaymentRepo()
    return PaymentService(repo)

@router.post('', status_code=201)
def create_customer(payload: dict, service: PaymentService = Depends(get_payment_service)):
    name = payload.get('name')
    email = payload.get('email')
    
    if name is None:
        raise HTTPException(status_code=400, detail="Name is required")
    elif len(name) > 100:
        raise HTTPException(status_code=400, detail="Name is too long")
    
    if email is None:
        raise HTTPException(status_code=400, detail="Email is required")
    
    customer = service.create_customer(name, email)
    return customer

@router.get("/{customer_id}")
def get_customer(customer_id: str, service: PaymentService = Depends(get_payment_service)):
    try:
        customer = service.get_customer(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

