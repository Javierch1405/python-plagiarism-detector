def promedio_movil(valores, ventana):
    if ventana <= 0 or ventana > len(valores):
        return []

    promedios = []
    for inicio in range(len(valores) - ventana + 1):
        bloque = valores[inicio : inicio + ventana]
        promedios.append(sum(bloque) / ventana)
    return promedios


def main():
    datos = [2, 4, 6, 8, 10]
    print(promedio_movil(datos, 3))


if __name__ == "__main__":
    main()