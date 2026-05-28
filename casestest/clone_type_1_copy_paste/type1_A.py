def calcular_promedio(calificaciones):
    suma = 0
    for calificacion in calificaciones:
        suma += calificacion

    if len(calificaciones) == 0:
        return 0

    return suma / len(calificaciones)


def main():
    datos = [80, 90, 100, 70]
    promedio = calcular_promedio(datos)
    print("Promedio:", promedio)


if __name__ == "__main__":
    main()
