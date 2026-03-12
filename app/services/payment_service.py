from app.utils.validators import (
    validate_amount,
    validate_currency,
    validate_email,
    generate_id,
)

class STATUS:
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class PaymentService:
    def __init__(self, repo):
        self.repo = repo
        
    def create_customer(self, name, email):
        if not name:
            raise ValueError("Name is required")
        if not validate_email(email):
            raise ValueError("Invalid email")
        
        existing_customer = self.repo.find_customer_by_email(email)
        if existing_customer:
            raise ValueError("Email already exists")
        
        customer = {
            'id': generate_id("cus"),
            'name': name,
            'email': email
        }
        return self.repo.save_customer(customer)
        
    
    def create_payment(self, customer_id, amount, currency):
        customer = self.repo.find_customer_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")
        
        if not validate_amount(amount):
            raise ValueError("Invalid amount")
        
        if not validate_currency(currency):
            raise ValueError("Invalid currency")
        
        payment = {
            'status': STATUS.PENDING,
            'id': generate_id('pay'),
            'amount': amount,
        }
        
        return self.repo.save_payment(payment)
    
    def capture(self, payment_id):
        return self._transition_status(
            payment_id=payment_id,
            required_status=STATUS.PENDING,
            new_status=STATUS.SUCCEEDED,
            error_message="Cannot capture",
        )
    
    def fail(self, payment_id):
        return self._transition_status(
            payment_id=payment_id,
            required_status=STATUS.PENDING,
            new_status=STATUS.FAILED,
            error_message="Cannot fail",
        )
        
    
    def refund(self, payment_id, amount):
        payment = self.repo.find_payment_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        
        if payment['status'] != STATUS.SUCCEEDED:
            raise ValueError("Cannot refund")
        
        refunds = self.repo.find_refunds_by_payment(payment_id)
        total_refunded = sum(refund['amount'] for refund in refunds)
        
        if total_refunded + amount > payment['amount']:
            raise ValueError("Refund exceeds payment amount")
        
        return payment 
    
    def get_payment(self, payment_id):
        return self.repo.find_payment_by_id(payment_id)

    def get_customer(self, customer_id):
        return self.repo.find_customer_by_id(customer_id)

    def get_payments_for_customer(self, customer_id):
        return self.repo.find_payments_by_customer(customer_id)
    
    def _transition_status(self, payment_id, required_status, new_status, error_message):
        payment = self.repo.find_payment_by_id(payment_id)
        if not payment:
            raise ValueError("Payment not found")
        
        if payment["status"] != required_status:
            raise ValueError(error_message)
        
        payment["status"] = new_status
        return self.repo.save_payment(payment)