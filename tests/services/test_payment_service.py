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
    
    def test_create_customer_generates_unique_id_prefixed_with_cus(self):
        customer = self.service.create_customer("Alice", "alice@example.com")
        self.assertTrue(customer['id'].startswith('cus_'))
    
    def test_create_customer_throws_name_is_required_when_name_empty(self):
        with self.assertRaisesRegex(ValueError, "Name is required"):
            self.service.create_customer("", "alice@example.com")
    
    def test_create_customer_throws_invalid_email(self):
        with self.assertRaisesRegex(ValueError, "Invalid email"):
            self.service.create_customer("Alice", "alice#example.com")
    
    def test_create_customer_throws_email_already_exists_email_registered_twice(self):
        self.service.create_customer("Alice", "alice@example.com")
        
        with self.assertRaisesRegex(ValueError, 'Email already exists'):
            self.service.create_customer("Alice", "alice@example.com")
    
    def test_create_payment_returns_payment_with_status_pending(self):
        customer = self.service.create_customer("Alice", "alice@example.com")
        payment = self.service.create_payment(customer['id'], 2999, 'usd')
        
        self.assertEqual(payment['status'], STATUS.PENDING)