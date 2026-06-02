def promedio(valores):
    return sum(valores) / len(valores) if valores else 0


if __name__ == "__main__":
    print(promedio([10, 20, 30, 40]))