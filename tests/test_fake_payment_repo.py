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