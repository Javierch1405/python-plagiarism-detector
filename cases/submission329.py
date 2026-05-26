def safe_factorial(n):
    if n < 0:
        return None
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res