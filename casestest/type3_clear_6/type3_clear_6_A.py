def invertir_palabras(texto):
    palabras = texto.split()
    palabras.reverse()
    return " ".join(palabras)


if __name__ == "__main__":
    print(invertir_palabras("una dos tres cuatro"))