def sumar_digitos(numero):
    if numero < 10:
        return numero
    return (numero % 10) + sumar_digitos(numero // 10)


if __name__ == "__main__":
    print(sumar_digitos(98765))