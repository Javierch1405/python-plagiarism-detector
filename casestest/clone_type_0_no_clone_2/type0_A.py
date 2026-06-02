def contar_palabras_unicas(texto):
    palabras = texto.lower().split()
    return len(set(palabras))


def main():
    ejemplo = "Hola mundo hola Python"
    print(contar_palabras_unicas(ejemplo))


if __name__ == "__main__":
    main()