def calcular_suma_pares(numeros):
    total = 0
    for numero in numeros:
        if numero % 2 == 0:
            total += numero
    return total


if __name__ == "__main__":
    print(calcular_suma_pares([1, 2, 3, 4, 5, 6]))