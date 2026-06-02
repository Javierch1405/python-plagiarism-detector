def existe_palabra(texto, palabra):
    return palabra.lower() in texto.lower().split()


if __name__ == "__main__":
    print(existe_palabra("hola mundo hola python", "hola"))