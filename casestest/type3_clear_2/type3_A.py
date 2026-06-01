def compute(a, b):
    """GCD por algoritmo de Euclides (módulo)"""
    a, b = abs(int(a)), abs(int(b))
    if b == 0:
        return a
    while b:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    print(compute(48, 18))
