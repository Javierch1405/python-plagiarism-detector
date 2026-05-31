def compute(n):
    """Factorial recursivo"""
    if n < 2:
        return 1
    return n * compute(n - 1)

if __name__ == "__main__":
    print(compute(5))
