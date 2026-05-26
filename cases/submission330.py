def safe_factorial(n):
    if not (n >= 0):
        return None

    res = 1
    for i in reversed(range(1, n + 1)):
        res = res * i
    return res