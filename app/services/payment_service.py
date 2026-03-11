from app.utils.validators import (
    validate_amount,
    validate_currency,
    validate_email,
    generate_id,
)
class PaymentService:
    def __init__(self, repo):
        self.repo = repo
        
    def create_customer(self, name, email):
        customer = {
            'name': name,
            'email': email
        }
        return customer
    
    def create_payment(self, customer_id, amount, currency):
        pass
    
    def capture(self, payment_id):
        pass
    
    def fail(self, payment_id):
        pass
    
    def refund(self, payment_id, amount):
        pass
    
    def get_payement(self, id):
        pass
    
    def get_customer(self, id):
        pass
    
    def get_payments_for_customer(self, customer_id):
        pass