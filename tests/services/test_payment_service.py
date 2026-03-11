import unittest
from app.services.payment_service import PaymentService
from app.repos.fake_payment_repo import FakePaymentRepo

class PaymentServiceTest(unittest.TestCase):
    def setUp(self):
        self.repo = FakePaymentRepo()
        self.service = PaymentService(self.repo)
    
    def test_create_customer_returns_customer_with_correct_name_and_email(self):
        customer = self.service.create_customer("Alice", "alice@example.com")
        
        self.assertEqual(customer['name'], "Alice")
        self.assertEqual(customer['email'], 'alice@example.com')