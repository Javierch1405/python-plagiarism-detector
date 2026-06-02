def calcular_producto_pares(numeros):
    producto = 1
    for numero in numeros:
        if numero % 2 == 0:
            producto *= numero
    return producto


if __name__ == "__main__":
    print(calcular_producto_pares([1, 2, 3, 4, 5, 6]))