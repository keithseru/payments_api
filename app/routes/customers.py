from fastapi import APIRouter, Depends, HTTPException
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

router = APIRouter()

def get_payment_service():
    repo = FakePaymentRepo()
    return PaymentService(repo)

