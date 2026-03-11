import uuid

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
    if "@" not in email or "." not in email:
        return False
    return True

def generateId(prefix) -> str:
    unique_part = uuid.uuid4().hex[6]
    return f"{prefix}_{unique_part}"