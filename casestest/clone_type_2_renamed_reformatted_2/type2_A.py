def sumar_pares(numeros):
    total = 0
    for numero in numeros:
        if numero % 2 == 0:
            total += numero
    return total


def main():
    datos = [1, 2, 3, 4, 5, 6]
    print(sumar_pares(datos))


if __name__ == "__main__":
    main()