class FakePaymentRepo:
    def __init__(self):
        self.customers = {}
        self.payments = {}
        self.refunds = {}

    def save_customer(self, customer):
        self.customers[customer["id"]] = customer
        return customer
    
    def find_customer_by_id(self, customer_id):
        return self.customers.get(customer_id)
    
    def find_customer_by_email(self, email):
        for customer in self.customers.values():
            if customer['email'] == email:
                return customer
        return None

    def save_payment(self, payment):
        self.payments[payment['id']] = payment
        return payment
    
    def find_payment_by_id(self, payment_id):
        return self.payments.get(payment_id)
    
    def find_payment_by_customer(self, customer_id):
        return [
            p for p in self.payments.values()
            if p['customerId'] == customer_id
        ]
    
    def save_refund(self, refund):
        self.refunds[refund["id"]] = refund
        return refund
    
    def find_refunds_by_payment(self, payment_id):
        return [
            refund for refund in self.refunds.values()
            if refund["paymentId"] == payment_id
        ]
    
    def clear(self):
        pass