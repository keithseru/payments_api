class FakePaymentRepo:
    def __init__(self):
        self.customers = {}
        self.payments = {}
        self.refunds = {}