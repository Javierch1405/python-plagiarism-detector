def calculate_power(base, exp):
    res = 1
    for _ in range(exp):
        res *= base
    return res