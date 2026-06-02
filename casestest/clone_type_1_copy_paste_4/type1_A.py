def generar_fibonacci(n):
    secuencia = [0, 1]
    while len(secuencia) < n:
        secuencia.append(secuencia[-1] + secuencia[-2])
    return secuencia[:n]


def main():
    print(generar_fibonacci(8))


if __name__ == "__main__":
    main()