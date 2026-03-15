import unittest
from unittest.mock import patch

from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

class TestPaymentServiceSpy(unittest.TestCase):
    def setUp(self):
        self.repo = FakePaymentRepo()
        self.service = PaymentService(self.repo)
        
    @patch('app.services.payment_service.logger.warn')
    def test_fail_logs_warning_with_payment_id(self, mock_warn):
        customer = self.service.create_customer("Alice", "alice@example.com")
        payment = self.service.create_payment(customer["id"], 2999, "usd")
        self.service.fail(payment["id"])

        mock_warn.assert_called_once()
        logged_message = mock_warn.call_args[0][0]
        self.assertIn(payment["id"], logged_message)
        
    @patch('app.services.payment_service.logger.warning')
    def test_fail_logs_warning_with_payment_id(self, mock_warning):
        customer = self.service.create_customer("Alice", "alice@example.com")
        payment = self.service.create_payment(customer["id"], 2999, "usd")
        self.service.fail(payment["id"])

        mock_warning.assert_called_once()


if __name__ == "__main__":
    unittest.main()