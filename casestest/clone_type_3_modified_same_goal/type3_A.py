def calcular_total_productos(productos):
    total = 0

    for producto in productos:
        precio = producto["precio"]
        cantidad = producto["cantidad"]
        total += precio * cantidad

    if total > 1000:
        total = total * 0.90

    return total


productos = [
    {"precio": 200, "cantidad": 2},
    {"precio": 150, "cantidad": 3},
    {"precio": 500, "cantidad": 1}
]

print(calcular_total_productos(productos))
