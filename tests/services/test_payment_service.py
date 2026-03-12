import unittest
from app.services.payment_service import PaymentService, STATUS
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
        
    def test_create_payment_generates_unique_idprefixed_with_pay(self):
        customer = self.service.create_customer("Alice", "alice@example.com")
        payment = self.service.create_payment(customer['id'], 2999, 'usd')
        self.assertTrue(payment["id"].startswith('pay_'))
        
    def test_create_payment_throw_error_when_customerid_unknown(self):
        with self.assertRaisesRegex (ValueError, "Customer not found"):
            self.service.create_payment('cus_unknown', 2999, "usd")   
    
    def test_create_payment_throws_error_when_amount_zero(self):
        customer = self.service.create_customer("Keith", 'keiht@email.com')
        with self.assertRaisesRegex(ValueError, "Invalid amount"):
            self.service.create_payment(customer['id'], 0, 'ugx')
    
    def test_create_payment_throws_error_when_amount_negative(self):
        customer = self.service.create_customer("Keith", 'keith@email.com')
        with self.assertRaisesRegex(ValueError, "Invalid amount"):
            self.service.create_payment(customer['id'], -20, 'ugx')
    
    def test_create_payment_throws_error_when_amount_decimal(self):
        customer = self.service.create_customer("Keith", 'keith@email.com')
        with self.assertRaisesRegex(ValueError, "Invalid amount"):
            self.service.create_payment(customer['id'], 9.99, 'ugx')
    
    def test_create_payment_throws_error_when_currency_not_three_chars(self):
        customer = self.service.create_customer("James", 'james@email.com')
        with self.assertRaisesRegex(ValueError, "Invalid currency"):
            self.service.create_payment(customer['id'], 2999, "abcd")
    
    def test_capture_chages_payment_status_from_pending_to_sucdeeded(self):
        customer = self.service.create_customer("James", 'james@email.com')
        payment = self.service.create_payment(customer['id'], 2999, 'ugx')
        
        updated = self.service.capture(payment['id'])
        
        self.assertEqual(updated['status'], STATUS.SUCCEEDED)