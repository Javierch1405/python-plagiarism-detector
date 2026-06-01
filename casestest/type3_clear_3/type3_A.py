def compute(n):
    """Chequeo primo simple (fuerza bruta)"""
    n = int(n)
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    print(compute(97))
