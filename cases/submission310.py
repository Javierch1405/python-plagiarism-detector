def apply_tax(amount):
    if amount > 1000:
        return amount * 1.15
    return amount * 1.05