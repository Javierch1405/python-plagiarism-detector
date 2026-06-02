def calcular_mcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)


if __name__ == "__main__":
    print(calcular_mcd(84, 30))