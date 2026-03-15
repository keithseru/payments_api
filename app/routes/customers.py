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
    
    customer = service.create_customer(name, email)
    return customer