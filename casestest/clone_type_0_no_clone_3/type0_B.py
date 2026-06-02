def generar_tabla_multiplicar(numero, limite):
    tabla = []
    for factor in range(1, limite + 1):
        tabla.append(numero * factor)
    return tabla


def main():
    print(generar_tabla_multiplicar(7, 5))


if __name__ == "__main__":
    main()