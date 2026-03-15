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

if __name__ == "__main__":
    unittest.main()