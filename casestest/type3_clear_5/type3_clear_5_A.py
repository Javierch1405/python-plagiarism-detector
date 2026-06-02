def sumar_digitos(numero):
    total = 0
    while numero > 0:
        total += numero % 10
        numero //= 10
    return total


if __name__ == "__main__":
    print(sumar_digitos(98765))