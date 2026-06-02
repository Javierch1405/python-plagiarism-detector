def contar_elementos_mayores_que(lista, umbral):
    contador = 0
    for elemento in lista:
        if elemento > umbral:
            contador += 1
    return contador


def main():
    print(contar_elementos_mayores_que([1, 5, 7, 2, 9], 4))


if __name__ == "__main__":
    main()