import unittest
from unittest.mock import MagicMock

from app.services.payment_service import PaymentService, STATUS

class TestPaymentServiceStub(unittest.TestCase):
    def test_capture_sets_status_to_succeeded_using_stub_repo(self):
        stub_repo = MagicMock()
        stub_repo.find_payment_by_id.return_value = {
            'id': "pay_1",
            'amount': 1000,
            'status': STATUS.PENDING
        }
        
        stub_repo.save_payment.side_effect = lambda payment: payment

        service = PaymentService(stub_repo)

        result = service.capture("pay_1")

        self.assertEqual(result["status"], STATUS.SUCCEEDED)

if __name__ == "__main__":
    unittest.main()