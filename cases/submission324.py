def calculate_power(base, exp):
    res = 1
    while exp > 0:
        res = res * base
        exp = exp - 1
    return res