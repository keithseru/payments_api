import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.routes.payments import get_payment_service

class TestPaymentRoutes(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock()
        app.dependency_overrides[get_payment_service] = lambda: self.mock_service
        self.client =TestClient(app)
    
    def tearDown(self):
        app.dependency_overrides.clear()
    
    def test_post_payments_returns_201_and_pending_payment_on_valid_input(self):
        self.mock_service.create_payment.return_value = {
            'id': 'pay_1',
            'customerId': 'cus_1',
            'amount': 2999,
            'currency': 'ugx',
            'status': 'pending',
        }
        
        response = self.client.post('/payments', json={
            'customerId': 'cus_1',
            'amount': 2999,
            'currency': 'ugx'
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], "pending")
        self.mock_service.create_payment.assert_called_once_with("cus_1", 2999, "ugx")
    
    def test_post_payment_retunrs_400_when_amount_missing(self):
        response = self.client.post('/payments', json={
            'customerId': 'cus_1',
            'currency': 'ugx',
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Amount is required")
    
    def test_post_payments_returns_400_when_currency_missing(self):
        response = self.client.post("/payments", json={
            "customerId": "cus_1",
            "amount": 2999,
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Currency is required")
    
    def test_post_payments_returns_400_when_customer_id_missing(self):
        response = self.client.post("/payments", json={
            "amount": 2999,
            "currency": "usd",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Customer ID is required")
    
    def test_post_payments_returns_500_when_service_throws_unexpectedly(self):
        self.mock_service.create_payment.side_effect = Exception("database exploded")

        response = self.client.post("/payments", json={
            "customerId": "cus_1",
            "amount": 2999,
            "currency": "ugx",
        })

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Something went wrong"})
    
    def test_post_capture_returns_200_and_updated_payment_when_successful(self):
        self.mock_service.capture.return_value = {
            "id": "pay_1",
            "status": "succeeded",
        }

        response = self.client.post("/payments/pay_1/capture")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "succeeded")
        self.mock_service.capture.assert_called_once_with("pay_1")
    
    def test_post_capture_returns_404_when_payment_not_found(self):
        self.mock_service.capture.side_effect = ValueError("Payment not found")

        response = self.client.post("/payments/pay_unknown/capture")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Payment not found")
    
    def test_post_capture_returns_409_when_payment_cannot_be_captured(self):
        self.mock_service.capture.side_effect = ValueError("Cannot capture")

        response = self.client.post("/payments/pay_1/capture")

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], "Cannot capture")
    
    def test_get_payments_returns_200_and_list_of_payments(self):
        self.mock_service.get_all_payments.return_value = [
            {
                "id": "pay_1",
                "customerId": "cus_1",
                "amount": 2999,
                "currency": "usd",
                "status": "pending",
            },
            {
                "id": "pay_2",
                "customerId": "cus_2",
                "amount": 5000,
                "currency": "usd",
                "status": "succeeded",
            },
        ]

        response = self.client.get("/payments")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
    
    def test_get_payments_returns_500_when_service_throws(self):
        self.mock_service.get_all_payments.side_effect = Exception("boom")

        response = self.client.get("/payments")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Something went wrong"})
    
    def test_post_payments_amount_of_1_returns_201(self):
        self.mock_service.create_payment.return_value = {
            "id": "pay_1",
            "customerId": "cus_1",
            "amount": 1,
            "currency": "usd",
            "status": "pending",
        }

        response = self.client.post("/payments", json={
            "customerId": "cus_1",
            "amount": 1,
            "currency": "usd",
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["amount"], 1)