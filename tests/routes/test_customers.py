import unittest 
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.routes.customers import get_payment_service

class TestCustomerRoutes(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock()
        app.dependency_overrides[get_payment_service] = lambda: self.mock_service
        self.client = TestClient(app)
    
    def tearDown(self):
        app.dependency_overrides.clear()
    
    def test_post_customers_returns_201_and_customer_on_valid_input(self):
        self.mock_service.create_customer.return_value = {
            'id': 'cus_1',
            'name': 'Keith',
            'email': 'keith@email.com',
        }
        
        response = self.client.post('/customers', json = {
            'name': 'Keith',
            'email': 'keith@email.com',
        })
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], "cus_1")
        self.assertEqual(response.json()["name"], "Keith")
        self.assertEqual(response.json()["email"], "keith@email.com")
        self.mock_service.create_customer.assert_called_once_with("Keith", "keith@email.com")
    
    def test_post_customers_returns_400_when_name_missing(self):
        response = self.client.post('/customers', json={
            'email': 'keith@email.com'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], 'Name is required')
    
    def test_post_customers_return_400_when_email_missing(self):
        response = self.client.post('/customers', json = {
            'name': 'Keith',
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], 'Email is required')
    
    def test_post_customers_doesnt_call_service_when_input_invalid(self):
        response = self.client.post('/customers', json ={
            'email': 'keith@email.com'
        })
        
        self.assertEqual(response.status_code, 400)
        self.mock_service.create_customer.assert_not_called()
    
    def test_post_customers_name_length_1_returns_201(self):
        self.mock_service.create_customer.return_value = {
            "id": "cus_1",
            "name": "A",
            "email": "a@example.com",
        }

        response = self.client.post("/customers", json={
            "name": "A",
            "email": "a@example.com",
        })

        self.assertEqual(response.status_code, 201)
    
    def test_post_customers_name_length_100_returns_201(self):
        long_name = "A" * 100
        self.mock_service.create_customer.return_value = {
            "id": "cus_1",
            "name": long_name,
            "email": "a@example.com",
        }

        response = self.client.post("/customers", json={
            "name": long_name,
            "email": "a@example.com",
        })

        self.assertEqual(response.status_code, 201)
    
    def test_post_customers_name_length_101_returns_400(self):
        long_name = "A" * 101
        self.mock_service.create_customer.side_effect = ValueError("Name is too long")

        response = self.client.post("/customers", json={
            "name": long_name,
            "email": "a@example.com",
        })

        self.assertEqual(response.status_code, 400)
    
    def test_get_customer_unknown_id_returns_404(self):
        self.mock_service.get_customer.return_value = None
        
        response = self.client.get('/customers/cus_unknown')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail':'Customer not found'})
    
    def test_get_customer_payments_unknown_customer_returns_404(self):
        self.mock_service.get_payments_for_customer.side_effect = ValueError("Customer not found")

        response = self.client.get("/customers/cus_unknown/payments")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'detail':'Customer not found'})

if __name__ == "__main__":
    unittest.main()