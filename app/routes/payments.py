from fastapi import APIRouter, Depends, HTTPException
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

router = APIRouter()


def get_payment_service():
    repo = FakePaymentRepo()
    return PaymentService(repo)

@router.post("", status_code=201)
def create_payment(payload: dict, service: PaymentService = Depends(get_payment_service)):
    customer_id = payload.get("customerId")
    amount = payload.get("amount")
    currency = payload.get("currency")
    
    payment = service.create_payment(customer_id, amount, currency)
    return payment