def contar_vocales(texto):
    total = 0
    for caracter in texto.lower():
        if caracter in "aeiou":
            total += 1
    return total


def main():
    print(contar_vocales("Arquitectura de software"))


if __name__ == "__main__":
    main()