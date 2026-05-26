def compute_factorial(n):
    result = 1
    for i in range(n, 1, -1):
        result = result * i
    return result