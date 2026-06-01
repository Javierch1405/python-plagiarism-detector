def compute(n):
    """Factorial iterativo"""
    result = 1
    i = 2
    while i <= n:
        result *= i
        i += 1
    return result

if __name__ == "__main__":
    print(compute(5))
