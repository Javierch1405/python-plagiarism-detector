def contar_consonantes(texto):
    consonantes = 0
    for caracter in texto.lower():
        if caracter.isalpha() and caracter not in "aeiou":
            consonantes += 1
    return consonantes


if __name__ == "__main__":
    print(contar_consonantes("Arquitectura de software"))