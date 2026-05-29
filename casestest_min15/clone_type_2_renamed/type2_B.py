def calcular_estadisticas(secuencia):
    suma = 0
    n = 0
    for elemento in secuencia:
        suma += elemento
        n += 1
    promedio = suma / n
    var = 0
    for elemento in secuencia:
        delta = elemento - promedio
        var += delta * delta
    var = var / n
    return promedio, var

def principal():
    valores = [7, 1, 9, 3, 5, 2]
    promedio, var = calcular_estadisticas(valores)
    print("promedio:", promedio)
    print("var:", var)

principal()
