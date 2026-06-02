def sumar_vocales(cadena):
    cantidad = 0
    for letra in cadena.lower():
        if letra in ["a", "e", "i", "o", "u"]:
            cantidad += 1
    return cantidad


def main():
    print(sumar_vocales("Arquitectura de software"))


if __name__ == "__main__":
    main()