def calcular_descuento(precio, porcentaje):
    descuento = precio * porcentaje / 100
    total = precio - descuento
    return total


def main():
    precio_original = 1200
    descuento = 15
    precio_final = calcular_descuento(precio_original, descuento)
    print("Precio final:", precio_final)


if __name__ == "__main__":
    main()
