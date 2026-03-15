from fastapi import APIRouter, Depends, HTTPException
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

router = APIRouter()

def get_payment_service():
    repo = FakePaymentRepo()
    return PaymentService(repo)

@router.post("", status_code=201)
def create_refund(payload: dict, service: PaymentService = Depends(get_payment_service)):
    payment_id = payload.get("paymentId")
    amount = payload.get("amount")

    if payment_id is None:
        raise HTTPException(status_code=400, detail="Payment ID is required")

    if amount is None:
        raise HTTPException(status_code=400, detail="Amount is required")

    try:
        refund = service.refund(payment_id, amount)
        return refund
    except ValueError as e:
        if str(e) == "Refund exceeds payment amount":
            raise HTTPException(status_code=422, detail=str(e))
        # catch other validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

@router.get("/{refund_id}")
def get_refund(refund_id: str, service: PaymentService = Depends(get_payment_service)):
    try:
        refund = service.get_refund(refund_id)
        if not refund:
            raise HTTPException(status_code=404, detail="Refund not found")
        return refund
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")