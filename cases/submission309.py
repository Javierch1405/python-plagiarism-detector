def apply_tax(amount):
    if amount > 1000:
        amount += amount * 0.15
    else:
        amount += amount * 0.05
    return amount