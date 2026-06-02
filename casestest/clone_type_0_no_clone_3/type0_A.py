def contar_lineas_no_vacias(texto):
    lineas = texto.splitlines()
    cantidad = 0
    for linea in lineas:
        if linea.strip():
            cantidad += 1
    return cantidad


def main():
    bloque = "uno\n\n dos\n\n tres\n"
    print(contar_lineas_no_vacias(bloque))


if __name__ == "__main__":
    main()