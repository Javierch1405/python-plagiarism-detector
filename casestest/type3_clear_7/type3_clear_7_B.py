def sumar_impares(numeros):
    return sum(numero for numero in numeros if numero % 2 != 0)


if __name__ == "__main__":
    print(sumar_impares([1, 2, 3, 4, 5, 6, 7]))