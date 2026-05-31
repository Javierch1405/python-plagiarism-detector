def compute(a, b):
    """GCD por resta repetida (método alternativo)"""
    a, b = abs(int(a)), abs(int(b))
    if a == 0:
        return b
    if b == 0:
        return a
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

if __name__ == "__main__":
    print(compute(48, 18))
