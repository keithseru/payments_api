import uuid

def validate_amount(amount):
    if not isinstance (amount, int):
        return False
    return amount > 0

def validate_currency(currency):
    if not isinstance (currency, str):
        return False
    if len(currency) < 3 or len(currency) > 3:
        return False
    return True

def validate_email(email):
    if "@" not in email or "." not in email:
        return False
    return True

def generate_id(prefix) -> str:
    unique_part = uuid.uuid4().hex[6]
    return f"{prefix}_{unique_part}"