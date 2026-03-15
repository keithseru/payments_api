import unittest
from app.repos.fake_payment_repo import FakePaymentRepo

class TestFakePaymentRepo(unittest.TestCase):
    def setUp(self):
        self.repo = FakePaymentRepo()
    
    def test_save_customer_stores_id_and_find_customer_returns_it(self):
        customer = {
            'id': "cus_1",
            'name': 'Bob',
            'email': 'bob@email.com',
        }
        
        self.repo.save_customer(customer)
        result = self.repo.find_customer_by_id('cus_1')
        
        self.assertEqual(result, customer)
        
    def test_find_customer_by_id_returns_none_for_unknown_id(self):
        result = self.repo.find_customer_by_id("cus_unknown")
        self.assertIsNone(result)
        
    def test_find_customer_by_email_returns_null_when_email_doesnt_match(self):
        customer = {
            'id': "cus_1",
            'name': 'Bob',
            'email': 'bob@email.com',
        }
        result = self.repo.find_customer_by_email("alice@email.com")
        self.assertIsNone(result)
    
    def test_find_customer_by_email_returns_customer_when_email_matches(self):
        customer = {
            'id': "cus_1",
            'name': 'James',
            'email': 'james@email.com',
        }
        self.repo.save_customer(customer)
        
        result = self.repo.find_customer_by_email('james@email.com')
        self.assertEqual(result, customer)
    
    def test_save_payment_stores_a_payment_so_find_payment_by_id_returns_it(self):
        payment = {
            'id': 'pay_1',
            'customerId': 'cus_1',
            'amount': '2999',
            'curency': 'ugx',
            'status': 'pending',
        }
        self.repo.save_payment(payment)
        result = self.repo.find_payment_by_id('pay_1')
        
        self.assertEqual(result, payment)