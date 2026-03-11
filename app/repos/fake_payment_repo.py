class FakePaymentRepo:
    def __init__(self):
        self.customers = {}
        self.payments = {}
        self.refunds = {}

    def save_customer(self, customer):
        self.customer[customer["id"]] = customer
        return customer
    
    def find_customer_by_id(self, customer_id):
        return self.customers.get(customer_id)
    
    def find_customer_by_email(self, email):
        for customer in self.customers.values():
            if customer['email'] == email:
                return customer
        return None