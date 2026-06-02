def es_palindromo(texto):
    texto_limpio = texto.lower().replace(" ", "")
    return texto_limpio == texto_limpio[::-1]


def main():
    print(es_palindromo("Anita lava la tina"))


if __name__ == "__main__":
    main()