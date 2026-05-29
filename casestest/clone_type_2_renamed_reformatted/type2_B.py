def obtener_importe(lista_items):
    acumulado = 0

    for item in lista_items:
        costo = item["precio"]
        unidades = item["cantidad"]
        acumulado += costo * unidades

    if acumulado > 1000:
        rebaja = acumulado * 0.10
        acumulado = acumulado - rebaja

    return acumulado


lista_items = [
    {"precio": 200, "cantidad": 2},
    {"precio": 150, "cantidad": 3},
    {"precio": 500, "cantidad": 1}
]

print(obtener_importe(lista_items))
