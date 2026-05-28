def buscar_mayor(numeros):
    mayor = numeros[0]

    for numero in numeros:
        if numero > mayor:
            mayor = numero

    return mayor


def main():
    valores = [4, 12, 7, 25, 9]
    print("Mayor:", buscar_mayor(valores))


if __name__ == "__main__":
    main()
