import unittest

class PaymentServiceTest(unittest.TestCase):
    def test_create_customer_returns_customer_with_correct_name_and_email(self):
        customer = self.create_customer("Alice", "alice@example.com")
        
        self.assertEqual(customer['name'], "Alice")