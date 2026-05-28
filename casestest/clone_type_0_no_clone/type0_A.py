def convertir_celsius_a_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


def main():
    temperatura = 25
    resultado = convertir_celsius_a_fahrenheit(temperatura)
    print("Fahrenheit:", resultado)


if __name__ == "__main__":
    main()
