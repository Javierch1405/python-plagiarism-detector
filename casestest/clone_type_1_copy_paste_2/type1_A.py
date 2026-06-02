def calcular_factorial(n):
    resultado = 1
    for numero in range(2, n + 1):
        resultado *= numero
    return resultado


def main():
    print(calcular_factorial(6))


if __name__ == "__main__":
    main()