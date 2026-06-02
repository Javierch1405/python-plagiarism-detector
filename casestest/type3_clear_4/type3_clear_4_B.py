def calcular_mcd(a, b):
    if b == 0:
        return abs(a)
    return calcular_mcd(b, a % b)


if __name__ == "__main__":
    print(calcular_mcd(84, 30))