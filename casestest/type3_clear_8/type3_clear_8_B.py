def contar_consonantes(texto):
    return sum(1 for caracter in texto.lower() if caracter.isalpha() and caracter not in "aeiou")


if __name__ == "__main__":
    print(contar_consonantes("Arquitectura de software"))