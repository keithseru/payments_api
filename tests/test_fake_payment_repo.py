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
    
    def test_find_payments_by_customer_returns_only_matching_payments(self):
        payment_1 = {
            "id": "pay_1",
            "customerId": "cus_1",
            "amount": 1000,
            "currency": "usd",
            "status": "pending",
        }
        payment_2 = {
            "id": "pay_2",
            "customerId": "cus_1",
            "amount": 2000,
            "currency": "usd",
            "status": "pending",
        }
        payment_3 = {
            "id": "pay_3",
            "customerId": "cus_2",
            "amount": 3000,
            "currency": "usd",
            "status": "pending",
        }

        self.repo.save_payment(payment_1)
        self.repo.save_payment(payment_2)
        self.repo.save_payment(payment_3)

        result = self.repo.find_payment_by_customer("cus_1")

        self.assertEqual(len(result), 2)
        self.assertIn(payment_1, result)
        self.assertIn(payment_2, result)
        self.assertNotIn(payment_3, result)
        
    def test_find_refunds_by_payment_returns_all_linked_refunds(self):
        refund_1 = {
            "id": "ref_1",
            "paymentId": "pay_1",
            "amount": 500,
            "status": "succeeded",
        }
        refund_2 = {
            "id": "ref_2",
            "paymentId": "pay_1",
            "amount": 300,
            "status": "succeeded",
        }
        refund_3 = {
            "id": "ref_3",
            "paymentId": "pay_2",
            "amount": 200,
            "status": "succeeded",
        }

        self.repo.save_refund(refund_1)
        self.repo.save_refund(refund_2)
        self.repo.save_refund(refund_3)

        result = self.repo.find_refunds_by_payment("pay_1")

        self.assertEqual(len(result), 2)
        self.assertIn(refund_1, result)
        self.assertIn(refund_2, result)
        self.assertNotIn(refund_3, result)
    
    def test_clear_empties_all_stored_data(self):
        self.repo.save_customer({
            "id": "cus_1",
            "name": "Alice",
            "email": "alice@example.com",
        })
        self.repo.save_payment({
            "id": "pay_1",
            "customerId": "cus_1",
            "amount": 1000,
            "currency": "usd",
            "status": "pending",
        })
        self.repo.save_refund({
            "id": "ref_1",
            "paymentId": "pay_1",
            "amount": 500,
            "status": "succeeded",
        })

        self.repo.clear()

        self.assertEqual(self.repo.customers, {})
        self.assertEqual(self.repo.payments, {})
        self.assertEqual(self.repo.refunds, {})  