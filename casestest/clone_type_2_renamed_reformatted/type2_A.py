def contar_vocales(texto):
    vocales = "aeiouAEIOU"
    contador = 0

    for letra in texto:
        if letra in vocales:
            contador += 1

    return contador


def main():
    frase = "Programacion en Python"
    total = contar_vocales(frase)
    print("Vocales encontradas:", total)


if __name__ == "__main__":
    main()
