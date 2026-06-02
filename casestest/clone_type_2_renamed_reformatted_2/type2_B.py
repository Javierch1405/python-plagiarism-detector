def totalizar_pares(lista_de_valores):
    acumulado = 0
    for valor in lista_de_valores:
        if valor % 2 == 0:
            acumulado = acumulado + valor
    return acumulado


def main():
    valores = [1, 2, 3, 4, 5, 6]
    print(totalizar_pares(valores))


if __name__ == "__main__":
    main()