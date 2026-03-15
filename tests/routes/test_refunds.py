import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.routes.refunds import get_payment_service

class TestRefundRoutes(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock()
        app.dependency_overrides[get_payment_service] = lambda: self.mock_service
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    def test_post_refunds_returns_201_and_refund_on_valid_input(self):
        self.mock_service.refund.return_value = {
            "id": "ref_1",
            "paymentId": "pay_1",
            "amount": 1000,
            "status": "succeeded",
        }

        response = self.client.post("/refunds", json={
            "paymentId": "pay_1",
            "amount": 1000,
        })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], "ref_1")
        self.mock_service.refund.assert_called_once_with("pay_1", 1000)
    
    def test_post_refunds_returns_400_when_payment_id_missing(self):
        response = self.client.post("/refunds", json={
            "amount": 1000,
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Payment ID is required")
    
    def test_post_refunds_returns_400_when_amount_missing(self):
        response = self.client.post("/refunds", json={
            "paymentId": "pay_1",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Amount is required")
    
    def test_post_refunds_returns_422_when_refund_exceeds_payment_amount(self):
        self.mock_service.refund.side_effect = ValueError("Refund exceeds payment amount")

        response = self.client.post("/refunds", json={
            "paymentId": "pay_1",
            "amount": 5000,
        })

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "Refund exceeds payment amount")