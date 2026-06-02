def validar_enteros(valores):
    for valor in valores:
        if not str(valor).isdigit():
            return False
    return True


if __name__ == "__main__":
    print(validar_enteros(["1", "x", "2", "3.5", "4"]))