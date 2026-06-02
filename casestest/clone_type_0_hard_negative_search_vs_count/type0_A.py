def contar_apariciones(texto, palabra):
    return texto.lower().split().count(palabra.lower())


if __name__ == "__main__":
    print(contar_apariciones("hola mundo hola python", "hola"))