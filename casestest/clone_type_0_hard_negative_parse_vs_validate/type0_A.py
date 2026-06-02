def parsear_enteros(valores):
    salida = []
    for valor in valores:
        try:
            salida.append(int(valor))
        except Exception:
            continue
    return salida


if __name__ == "__main__":
    print(parsear_enteros(["1", "x", "2", "3.5", "4"]))