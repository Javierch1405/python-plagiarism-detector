def invertir_palabras(texto):
    return " ".join(reversed(texto.split()))


if __name__ == "__main__":
    print(invertir_palabras("una dos tres cuatro"))