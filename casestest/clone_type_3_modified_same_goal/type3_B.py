def aplicar_descuento(monto):
    if monto <= 1000:
        return monto
    return monto * 0.90


def calcular_pago(items):
    subtotal = sum(
        item["precio"] * item["cantidad"]
        for item in items
    )

    return aplicar_descuento(subtotal)


items = [
    {"precio": 200, "cantidad": 2},
    {"precio": 150, "cantidad": 3},
    {"precio": 500, "cantidad": 1}
]

resultado = calcular_pago(items)
print(resultado)
