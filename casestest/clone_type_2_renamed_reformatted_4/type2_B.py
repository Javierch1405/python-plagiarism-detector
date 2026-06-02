def total_de_mayores(valores, limite):
    cantidad = 0
    for valor in valores:
        if valor > limite:
            cantidad = cantidad + 1
    return cantidad


def main():
    print(total_de_mayores([1, 5, 7, 2, 9], 4))


if __name__ == "__main__":
    main()