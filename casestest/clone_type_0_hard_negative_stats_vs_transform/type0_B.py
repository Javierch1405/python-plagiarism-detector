def normalizar(valores):
    if not valores:
        return []
    minimo = min(valores)
    maximo = max(valores)
    if minimo == maximo:
        return [0 for _ in valores]
    return [(valor - minimo) / (maximo - minimo) for valor in valores]


if __name__ == "__main__":
    print(normalizar([10, 20, 30, 40]))