def validateAmount(amount):
    if not isinstance (amount, int):
        return False
    return amount > 0

def validateCurrency(currency):
    if not isinstance (currency, str):
        return False
    if len(currency) < 3 or len(currency) > 3:
        return False
    return True

def validateEmail(email):
    pass

def generateId(prefix):
    pass