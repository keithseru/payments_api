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
    
    if amount is None:
        raise HTTPException(status_code=400, detail="Amount is required")
    elif not isinstance(amount, int) or amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")
        
    
    if currency is None:
        raise HTTPException(status_code=400, detail="Currency is required")
    
    if customer_id is None:
        raise HTTPException(status_code=400, detail="Customer ID is required")
    
    
    try:
        payment = service.create_payment(customer_id, amount, currency)
        return payment
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.post("/{payment_id}/capture")
def capture_payment(payment_id: str, service: PaymentService = Depends(get_payment_service)):
    try:
        payment = service.capture(payment_id)
        return payment
    except ValueError as e:
        if str(e) == "Payment not found":
            raise HTTPException(status_code=404, detail=str(e))
        if str(e) == "Cannot capture":
            raise HTTPException(status_code=409, detail=str(e))

@router.get("")
def list_payments(service: PaymentService = Depends(get_payment_service)):
    try:
        return service.get_all_payments()
    except: 
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get("/{payment_id}")
def get_payment(payment_id: str, service: PaymentService = Depends(get_payment_service)):
    try:
        payment = service.get_payment(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail ="Payment not found")
        return payment
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail ="Something went wrong")