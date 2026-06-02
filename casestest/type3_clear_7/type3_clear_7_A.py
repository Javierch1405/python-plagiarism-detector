def sumar_impares(numeros):
    total = 0
    for numero in numeros:
        if numero % 2 != 0:
            total += numero
    return total


if __name__ == "__main__":
    print(sumar_impares([1, 2, 3, 4, 5, 6, 7]))