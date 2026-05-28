def obtener_maximo(lista):
    lista_ordenada = sorted(lista)
    return lista_ordenada[-1]


def main():
    datos = [4, 12, 7, 25, 9]
    maximo = obtener_maximo(datos)
    print("Mayor:", maximo)


if __name__ == "__main__":
    main()
